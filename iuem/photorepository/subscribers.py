# -*- coding: utf-8 -*-
from PIL import Image , ImageDraw
from cStringIO import StringIO
from iuem.photorepository.extender import ImageImageRepositoryExtender 
from iuem.photorepository.extender import FolderImageRepositoryExtender
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer


# @adapter(IATImage , IObjectInitializedEvent)
def createSmallImage(obj, event):
    def __init__(self , context):
        self.context = context
    # copy the image loaded to 'original' (extended) field
    ImageImageRepositoryExtender(obj).fields[0].set(obj , obj.getImage())
    # reduce the image field and add the watermark
    doThumbnail(obj)
    #
    # import pdb;pdb.set_trace()
    
def doThumbnail(obj):
    f_uploaded =  obj.getImageAsFile()
    uploaded = Image.open(f_uploaded)
    if uploaded.mode != 'RGBA':
        uploaded = uploaded.convert('RGBA')
    size = 300 , 300
    uploaded.thumbnail(size, Image.ANTIALIAS)
    draw = ImageDraw.Draw(uploaded)
    draw.line((0, 0) + uploaded.size, fill=(255, 255, 255))
    draw.line((0, uploaded.size[1], uploaded.size[0], 0), fill=(255, 255, 255))
    f_data = StringIO()
    uploaded.save(f_data , 'jpeg')
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
