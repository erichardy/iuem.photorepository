# -*- coding: utf-8 -*-
from PIL import Image , ImageDraw
from PIL import ImageChops
from StringIO import StringIO
from iuem.photorepository.extender import ImageImageRepositoryExtender 
from iuem.photorepository.extender import FolderImageRepositoryExtender
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.app.imaging.traverse import DefaultImageScaleHandler
from Products.Archetypes.event import ObjectEditedEvent , ObjectInitializedEvent

def installRepoImage(obj, event):
    f_uploaded =  obj.getImageAsFile()
    ImageImageRepositoryExtender(obj).fields[0].set(obj , obj.getImage())
    exif = ImageImageRepositoryExtender(obj).context.getEXIF()
    ImageImageRepositoryExtender(obj).fields[12].set(obj , exif)
    doThumbnail(obj)    

def updateRepoImage(obj, event):
    """
    """
    if not isinstance(event,ObjectEditedEvent):
        return
    request = obj.REQUEST
    # If the image field was modified...
    if request.form.has_key('image_file'):
        if request.form['image_file'].filename != '':
            ImageImageRepositoryExtender(obj).fields[0].set(obj ,obj.getImage())
            exif = ImageImageRepositoryExtender(obj).context.getEXIF()
            ImageImageRepositoryExtender(obj).fields[12].set(obj , exif)
            doThumbnail(obj)

def createSmallImage(obj, event):
    # copy the image loaded to 'original' (extended) field
    f_uploaded =  obj.getImageAsFile()
    currentImage = Image.open(f_uploaded)
    ImageImageRepositoryExtender(obj).fields[0].set(obj , f_uploaded.read())
    exif = ImageImageRepositoryExtender(obj).context.getEXIF()
    ImageImageRepositoryExtender(obj).fields[12].set(obj , exif) 
    doThumbnail(obj)
    
def sameImages(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def doThumbnail(obj):
    # f_uploaded =  obj.getImageAsFile()
    # uploaded = Image.open(f_uploaded)
    field = obj.getField('image')
    scaled = DefaultImageScaleHandler(field).getScale(obj, scale='large')
    f_image = StringIO(scaled.data)
    image = Image.open(f_image)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    size = 300 , 300
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
    portal = obj.portal_url.getPortalObject()
    try:
        myVocabsTool = getToolByName(portal , ATVOCABULARYTOOL)
    except:
        print 'Products.ATVocabularyManager not yet installed... skipped'
        return
    vocabs = getVocabularies(obj)
    normalizer = getUtility(INormalizer)
    # import pdb;pdb.set_trace()
    for k in vocabs.keys():
        # parse each vocabulary : myVocab is the vocabulary associated with a key
        myVocab = myVocabsTool[vocabs[k]]
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
            i = nbField(obj,k)
            if obj.portal_type == 'Image':
                ImageImageRepositoryExtender(obj).fields[i].set(obj,newMetadatas)
            else:
                FolderImageRepositoryExtender(obj).fields[i].set(obj,newMetadatas)
                
        