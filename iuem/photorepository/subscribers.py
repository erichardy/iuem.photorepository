from Products.ATContentTypes.interface import IATImage
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent
from PIL import Image , ImageDraw
from cStringIO import StringIO
from iuem.photorepository.extender import imPhotoSmallImageExtender 

@adapter(IATImage , IObjectInitializedEvent)
def createSmallImage(obj, event):
    def __init__(self , context):
        self.context = context
    if 'imPhoto' not in obj.aq_parent.getImmediatelyAddableTypes():
        # no imPhoto in this container: we do nothing
        return
    # copy the image loaded to 'original' (extended) field
    imPhotoSmallImageExtender(obj).fields[0].set(obj , obj.getImage())
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
    