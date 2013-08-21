# -*- coding: utf-8 -*-
import logging
from PIL import Image , ImageEnhance
from StringIO import StringIO
from iuem.photorepository.extender import ImageImageRepositoryExtender 
from iuem.photorepository.extender import FolderImageRepositoryExtender
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.app.imaging.traverse import DefaultImageScaleHandler
from Products.Archetypes.event import ObjectEditedEvent
from zope.traversing.api import traverse

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

def restoreFull(obj):
    if obj.portal_type != 'Image':
            return
    source = obj.getField("sourceImage")
    obj.setImage(source.get(obj).data)

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def hasWatermark(obj):
    logger.info('hasWatermark ? ' + obj.title)
    try:
        wm = obj.getField('watermark')
    except:
        return False
    return wm.getSize(obj) != (0,0)

def searchWatermark(obj):
    """
    this function returns a watermark for the object:
    if the object has a empty watermark field,
    it is searched to it's parent, and if it's parent doesn't have,
    it is searched until to reach the root plone site
    If, there is no watermark, the registry watermark is returned if there is one
    elsewhere, False is returned
    NB: the watermark must be an image with tranparency 
    """
    if hasWatermark(obj):
        wm = obj.getField('watermark').get(obj).data
        mark = Image.open(StringIO(wm))
        return mark
    while obj.aq_parent.portal_type == 'Folder':
        if hasWatermark(obj):
            wm = obj.getField('watermark').get(obj).data
            mark = Image.open(StringIO(wm))
            return mark
        obj = obj.aq_parent
    registry = getUtility(IRegistry)
    globalWatermark_name = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.watermark_image_name']
    try:
        globalWatermark = traverse(obj , 'portal_skins/custom/' + globalWatermark_name)
        wm = Image.open(StringIO(globalWatermark.data))
        return wm
    except:
        logger.info('WARNING! no watermark applied !... no global watermark found...')
        return False

def getPosition(image , wm):
    li = image.size[0]
    hi = image.size[1]
    lw = wm.size[0]
    hw = wm.size[1]
    # if watermark is larger than image, reduce it to image size
    if ((lw > li) or (hw > hi)):
        wm.thumbnail(image.size , Image.ANTIALIAS)
        lw = wm.size[0]
        hw = wm.size[1]
        logger.info('reduce wm')
    registry = getUtility(IRegistry)
    wmPosition = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.watermark_position']
    if wmPosition == 'center':
        position = ((li - lw) / 2 , (hi - hw) / 2)
    elif wmPosition == 'topleft':
        position = (0,0) 
    elif wmPosition == 'topright':
        position = ((li - lw) , 0)
    elif wmPosition == 'bottomleft':
        position = (0 , (hi - hw))
    elif wmPosition == 'bottomright':
        position = ((li - lw) , (hi - hw))
    else:
        position = ((hi - hw) , (li - lw))
    # logger.info('Position : ' + wmPosition + ' ' + str(position))
    return position


# thanks to http://pydoc.net/Python/unweb.watermark/0.3/unweb.watermark.subscribers/
# docs for PIL : http://python.developpez.com/cours/pilhandbook/
def doThumbnail(obj):
    title00 = (obj.getField('title').get(obj)[:3] == '00-')
    if title00:
        return False
    # we don't want to apply a watermark on a watermarked image
    restoreFull(obj)
    field = obj.getField('image')
    scaled = DefaultImageScaleHandler(field).getScale(obj, scale='large')
    f_image = StringIO(scaled.data)
    image = Image.open(f_image)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    size = 600 , 600
    image.thumbnail(size, Image.ANTIALIAS)
    wm = searchWatermark(obj)
    position = getPosition(image , wm)
    if wm:
        image.paste(wm , position , wm)
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
        if (k == 'photographer'):
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