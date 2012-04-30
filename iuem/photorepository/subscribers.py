from Products.ATContentTypes.interface import IATImage
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from PIL import Image , ImageDraw
from cStringIO import StringIO
from iuem.photorepository.extender import ImageImageRepositoryExtender 
from iuem.photorepository.extender import FolderImageRepositoryExtender
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL


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

# obj and event.object are identical
def updateVocabularies(obj , event):
    """update vocabularies according to new values entered"""
    vocabs = getVocabularies(obj)
    for k in vocabs.keys():
        myVocabsTool = getToolByName(obj.portal_url.getPortalObject() , ATVOCABULARYTOOL)
        vocabulary = myVocabsTool[vocabs[k]]
        for word in obj[k]:
            if not hasattr(vocabulary , word):
                vocabulary.invokeFactory('SimpleVocabularyTerm', word)
                vocabulary[word].setTitle(word)
        
        
    # import pdb;pdb.set_trace()
    pass