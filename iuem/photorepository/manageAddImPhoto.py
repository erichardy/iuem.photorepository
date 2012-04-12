from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.event import notify

from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.Archetypes.event import ObjectInitializedEvent


def ObjectAddedEvent(self):
    print "Event : ObjectAddedEvent\n"
    
def ObjectCreatedEvent(self):
    print "Event : ObjectCreatedEvent\n"

def ContainerModifiedEvent(self):
    print "Event : ContainerModifiedEvent\n"
    
def WriteContainer(self):
    print "Event : WriteContainer\n"
    
class IcreateimPhotoEvent(Interface , IObjectInitializedEvent):
    """event fired when a imPhoto is created
    """
    context = Attribute("The content object that was created")

class creatimPhotoEvent(object):
    """Event notified when an imPhoto is created
    """
    implements(IcreateimPhotoEvent)
    def __init__(self , context):
        self.context = context

def createimPhotoHandler(self):
    print "++++.... createimPhotoHandler"

def ehObjectInitializedEvent(obj):
    def __init__(self , context):
        self.context = context
    
    print "....ObjectInitializedEvent"
    print "obj = " + str(obj)
    print "Object dictionnary : "
    print obj.object.__dict__
    print "==============================="
    print "obj.object.title = " + str(obj.object.title)
    print "obj.object.id = " + str(obj.object.id)
    
    
    # import pdb;pdb.set_trace()
    

