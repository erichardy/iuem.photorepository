from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.event import notify

from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.Archetypes.event import ObjectInitializedEvent

from cStringIO import StringIO
from PIL import Image , ImageDraw , ImageEnhance

"""
links : http://code.activestate.com/recipes/362879-watermark-with-pil/
http://blog.objectgraph.com/index.php/2009/04/02/python-quick-watermark-example-with-pil/
http://www.geeks3d.com/20100930/tutorial-first-steps-with-pil-python-imaging-library/#p06

"""

def imPhotoObjectInitializedEvent(obj):
    def __init__(self , context):
        self.context = context
    """
    print "....ObjectInitializedEvent"
    print "obj = " + str(obj)
    print "Object dictionnary : "
    print obj.object.__dict__
    print "==============================="
    print "obj.object.title = " + str(obj.object.title)
    print "obj.object.id = " + str(obj.object.id)
    print "nom de l'imPhotoSmall : " + imPhotoSmallName(obj.object.id)
    """
    rawImage = obj.object.getImageAsFile()
    smallImage = Image.open(rawImage)
    if smallImage.mode != 'RGBA':
        smallImage = smallImage.convert('RGBA')
    # imPhotoSmall processing   
    size = 300 , 300
    smallImage.thumbnail(size, Image.ANTIALIAS)
    draw = ImageDraw.Draw(smallImage)
    draw.line((0, 0) + smallImage.size, fill=(255, 255, 255))
    draw.line((0, smallImage.size[1], smallImage.size[0], 0), fill=(255, 255, 255))
    #
    name = imPhotoSmallName(obj.object.id)
    f_data = StringIO()
    smallImage.save(f_data , 'jpeg')
    newSmallImage = f_data.getvalue()
    obj.object.aq_parent.invokeFactory('imPhotoSmall',name,image=newSmallImage)
    
    # import pdb;pdb.set_trace()
    
def imPhotoSmallName(imPhotoName):
    """return a name for an imPhotoSmall from an imPhoto name (an id)
    """
    nameSplited = imPhotoName.split('.')
    extention = nameSplited[len(nameSplited) - 1]
    basename = imPhotoName.rstrip(extention).rstrip('.')
    return basename + '_imPhotoSmall_' + '.' + extention



