# -*- coding: utf-8 -*-
import logging
from PIL import Image , ImageDraw
from StringIO import StringIO
from iuem.photorepository.extender import ImageImageRepositoryExtender 
from iuem.photorepository.extender import FolderImageRepositoryExtender
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.app.imaging.traverse import DefaultImageScaleHandler
from Products.Archetypes.event import ObjectEditedEvent

logger = logging.getLogger('iuem.photorepository')


def getObjectEvents(obj, event):
    """
    some debugging to do !!!
    see : http://plone.org/documentation/manual/developer-manual/archetypes/other-useful-archetypes-features/how-to-use-events-to-hook-the-archetypes-creation-process/
    
    """
    logger.info('getObjectEvents: ' + str(event) + ' ' + str(obj.Title()))
    mmm = obj.getField('sourceImage').get(obj)
    imageSize = mmm.getSize()
    if imageSize == (0,0):
        logger.info('getObjectEvents: size = ' + str(mmm.getSize()))
    else:
        logger.info('getObjectEvents: size = pas zero,zero')
    # import pdb;pdb.set_trace()
    
def setSourceimageAndExif(obj, sourceImage):
    obj.getField("sourceImage").set(obj , sourceImage)
    exif = ImageImageRepositoryExtender(obj).context.getEXIF()
    obj.getField("exif").set(obj, exif)

def installRepoImage(obj, event):
    sourceImageSize = obj.getField('sourceImage').get(obj).getSize()
    # msg = 'installRepoImage: before call to setSourceimageAndExif... '
    # msg = msg + str(sourceImageSize)
    # logger.info(msg)
    # sometimes, IObjectInitializedEvent is sent even no appropriate
    # so, we don't want that the original image is replaced by the
    # transformed one
    notYetAnImage = (sourceImageSize == (0,0))
    if notYetAnImage:
        setSourceimageAndExif(obj, obj.getImage())
    # we want that some images are not processed : when title tarts with '00-'
    no00title = (obj.getField('title').get(obj)[:3] != '00-')
    if no00title:
        doThumbnail(obj)


def updateRepoImage(obj, event):
    if not isinstance(event,ObjectEditedEvent):
        return
    request = obj.REQUEST
    # If the image field was modified...
    if request.form.has_key('image_file'):
        if request.form['image_file'].filename != '':
            setSourceimageAndExif(obj, obj.getImage())
            if obj.getField('title').get(obj)[:3] != '00-':
                # logger.info('updateRepoImage: just before call doThum...')
                doThumbnail(obj)

def createSmallImage(obj, event):
    # copy the image loaded to 'sourceImage' (extended) field
    f_uploaded =  obj.getImageAsFile()
    setSourceimageAndExif(obj, f_uploaded.read())
    doThumbnail(obj)

def doThumbnail(obj):
    field = obj.getField('image')
    scaled = DefaultImageScaleHandler(field).getScale(obj, scale='large')
    f_image = StringIO(scaled.data)
    image = Image.open(f_image)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    size = 600 , 600
    image.thumbnail(size, Image.ANTIALIAS)
    draw = ImageDraw.Draw(image)
    draw.line((0, 0) + image.size, fill=(255, 255, 255))
    draw.line((0, image.size[1], image.size[0], 0), fill=(255, 255, 255))
    f_data = StringIO()
    image.save(f_data , 'jpeg')
    obj.setImage(f_data.getvalue())

def getVocabularies(obj):
    """return a dictionary : ['field'] = 'associated vocabulary name'
    """
    fields = []
    vocabs = {}
    myType = obj.Type()
    if myType == 'Image':
        fields = ImageImageRepositoryExtender(obj).fields
    elif myType == 'Folder':
        fields = FolderImageRepositoryExtender(obj).fields
    else:
        return vocabs

    for field in fields:
        try:
            vocab_name = field.vocabulary.vocab_name
            name = field.getName()
            vocabs[name] = vocab_name
        except:
            pass
    return vocabs

def cleanupKeywords(keywordsList):
    """delete entries when they are the same but upper/lower case
       delete empty entries : '' or ' ' 
    TODO....
    """
    newKeywordsList = [ x for x in keywordsList ]
    #
    # code to cleanup newKeywordsList here...
    # 
    return newKeywordsList

def nbField(obj , name):
    """returns the field number of the named field in the extended schema"""
    if obj.portal_type == 'Image':
        for i in range(0,len(ImageImageRepositoryExtender(obj).fields)):
            if ImageImageRepositoryExtender(obj).fields[i].getName() == name:
                return i
    else:
        for i in range(0,len(FolderImageRepositoryExtender(obj).fields)):
            if FolderImageRepositoryExtender(obj).fields[i].getName() == name:
                return i

# obj and event.object are identical
def updateVocabularies(obj , event):
    """update vocabularies according to new values entered"""
    try:
        myVocabsTool = getToolByName(obj , ATVOCABULARYTOOL)
    except :
        msg = 'Products.ATVocabularyManager not yet installed... skipped'
        logger.info(msg)
        return
    vocabs = getVocabularies(obj)
    normalizer = getUtility(INormalizer)
    for k in vocabs.keys():
        # parse each vocabulary : myVocab is the vocabulary associated with a key
        myVocab = myVocabsTool[vocabs[k]]
        if k == 'photographer':
            # logger.info('pour photographer...' + k + '/' + obj[k].decode('utf-8'))
            # import pdb;pdb.set_trace()
            kword = obj[k]
            ukword = unicode(kword,'utf-8')
            normalizedWord = normalizer.normalize(ukword, locale = 'fr')
            if not kword in myVocab.getVocabularyDict().keys():
                if kword != '':
                    myVocab.addTerm(normalizedWord , kword , silentignore=True)
            obj.getField(k).set(obj, normalizedWord)
        else:
            # logger.info('k = ' + k)
            # should call cleanupKeywords(obj[k])
            if '' in obj[k]: obj[k].remove('')
        
            needToCorrect = False
            for kword in obj[k]:
                ukword = unicode(kword,'utf-8')
                if not kword in myVocab.getVocabularyDict().keys():
                    normalizedWord = normalizer.normalize(ukword, locale = 'fr')
                    myVocab.addTerm(normalizedWord , kword , silentignore=True)
                needToCorrect = True
            if needToCorrect:
            # replace the new metadata by the corresponding key in the vocabulary
                newMetadatas = []
                for kword in obj[k]:
                    ukword = unicode(kword,'utf-8')
                    normalizedWord = normalizer.normalize(ukword, locale = 'fr')
                    if kword == normalizedWord:
                        newMetadatas.append(kword)
                    else:
                        newMetadatas.append(normalizedWord)
                obj.getField(k).set(obj, newMetadatas)
        
def nextPrevious(obj,event):
    obj.setNextPreviousEnabled("True")    