from Products.ATContentTypes.interface import IATImage
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent, IObjectEditedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent
from plone.app.blob.scale import BlobImageScaleHandler
from plone.app.imaging.traverse import DefaultImageScaleHandler
from PIL import Image, ImageEnhance
from cStringIO import StringIO
import urllib
import os
import tempfile
from Products.CMFCore.utils import getToolByName
from iuem.photorepository.extender import imPhotoSmallImageExtender 

@adapter(IATImage , IObjectInitializedEvent)
def createSmallImage(obj, event):
    if 'imPhoto' not in obj.aq_parent.getImmediatelyAddableTypes():
        print "pas l'imPhoto ici"
        import pdb;pdb.set_trace()
        return
    print "OK..."
    import pdb;pdb.set_trace()
    