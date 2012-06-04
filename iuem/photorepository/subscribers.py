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
from  Products.Archetypes.event import ObjectEditedEvent , ObjectInitializedEvent

def installRepoImage(obj, event):
    # print 'entree dans installRepoImage.'
    f_uploaded =  obj.getImageAsFile()
    # currentImage = Image.open(f_uploaded)
    ImageImageRepositoryExtender(obj).fields[0].set(obj , obj.getImage())
    exif = ImageImageRepositoryExtender(obj).context.getEXIF()
    print exif
    ImageImageRepositoryExtender(obj).fields[12].set(obj , exif)
    # import pdb;pdb.set_trace()
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
            # print exif
            ImageImageRepositoryExtender(obj).fields[12].set(obj , exif)
            doThumbnail(obj)

# @adapter(IATImage , IObjectInitializedEvent)
def createSmallImage(obj, event):
    # copy the image loaded to 'original' (extended) field
    # ImageImageRepositoryExtender(obj).fields[0].copy(obj.getImage())
    f_uploaded =  obj.getImageAsFile()
    currentImage = Image.open(f_uploaded)
    # f_sourceImage = ImageImageRepositoryExtender(obj).fields[0].getRaw(obj).getBlob().committed()
    # sourceImage = Image.open(f_sourceImage)
    """
    if sameImages(currentImage , sourceImage):
        print "Images identiques"
        return
    else:
        print "pas pareilles..."
    """
    import pdb;pdb.set_trace()
    ImageImageRepositoryExtender(obj).fields[0].set(obj , f_uploaded.read())
    exif = ImageImageRepositoryExtender(obj).context.getEXIF()
    ImageImageRepositoryExtender(obj).fields[12].set(obj , exif) 
    print exif
        # reduce the image field and add the watermark
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
    

# obj and event.object are identical
def updateVocabularies(obj , event):
    """update vocabularies according to new values entered"""
    portal = obj.portal_url.getPortalObject()
    myVocabsTool = getToolByName(portal , ATVOCABULARYTOOL)
    vocabs = getVocabularies(obj)
    normalizer = getUtility(INormalizer)
    for k in vocabs.keys():
        myVocab = myVocabsTool[vocabs[k]]
        # print 'k = ' + str(k) + ' ' + str(myVocab)
        # should call cleanupKeywords(obj[k])
        if '' in obj[k]: obj[k].remove('')
        for kword in obj[k]:
            ukword = unicode(kword,'utf-8')
            normalizedWord = normalizer.normalize(ukword, locale = 'fr')
            if not hasattr(myVocab , normalizedWord):
                # myVocab.invokeFactory('SimpleVocabularyTerm', normalizedWord , title = word)
                # myVocab[normalizedWord].setTitle(word)
                myVocab.addTerm(normalizedWord , kword)
        
    # import pdb;pdb.set_trace()
    """
    widget_addremove.pt modified !!!! : line 98
                      <tal:block repeat="item vocabulary/keys">
                    <option
                        value="#"
                        tal:define="val python:vocabulary.getValue(item)"
                        tal:condition="python:not val in selectedItems"
                        tal:content="python:vocabulary.getValue(item)"
                        tal:attributes="value val;">Item</option>
                  </tal:block>
    """
