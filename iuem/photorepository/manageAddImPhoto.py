from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.event import notify

from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.Archetypes.event import ObjectInitializedEvent

from PIL import Image , ImageDraw

"""
creation process of an imPhotoSmall derived from an imPhoto :
- the name of the imPhotoSmall is the basename of the imPhoto added by 
  '_imPhotoSmall' and the extension of the imPhoto
- if the size of the imPhoto is less than the standard size of imPhotoSmall, the
  original size is kept 
- a watermark is added to the imPhotoSmall
- the imPhotoSmall is created
- the dictionary of imPhotoSmall metadatas is created for this imPhotoSmall
  (annotations)

Note: the watermark is first looked up in the dictionary of the containers
imAlbum and if there is no such watermark in any of the parents containers, the
global one is used.

links : http://code.activestate.com/recipes/362879-watermark-with-pil/
http://blog.objectgraph.com/index.php/2009/04/02/python-quick-watermark-example-with-pil/
http://www.geeks3d.com/20100930/tutorial-first-steps-with-pil-python-imaging-library/#p06

"""

def imPhotoObjectInitializedEvent(obj):
    def __init__(self , context):
        self.context = context
    
    print "....ObjectInitializedEvent"
    print "obj = " + str(obj)
    print "Object dictionnary : "
    print obj.object.__dict__
    print "==============================="
    print "obj.object.title = " + str(obj.object.title)
    print "obj.object.id = " + str(obj.object.id)
    print "nom de l'imPhotoSmall : " + imPhotoSmallName(obj.object.id)
    
    # rawImage = ImageDraw.Draw(obj.object.getImageAsFile())
    # smallImage = rawImage.thumbnail((400,600) , Image.ANTIALIAS)
    # OK rawImage = obj.object.getImageAsFile()
    rawImage = obj.object.getImage()
    # smallRawImage = Image.frombuffer(Image.RGBX ,obj.object.getSize() ,rawImage)
    # smallImage = smallRawImage
    # name = imPhotoSmallName(obj.object.id)
    # obj.object.aq_parent.invokeFactory('imPhotoSmall',name,image=smallImage)
    
    import pdb;pdb.set_trace()
    
def imPhotoSmallName(imPhotoName):
    """return a name for an imPhotoSmall from an imPhoto name (an id)
    """
    nameSplited = imPhotoName.split('.')
    extention = nameSplited[len(nameSplited) - 1]
    basename = imPhotoName.rstrip('.' + extention)
    return basename + '_imPhotoSmall_' + '.' + extention



