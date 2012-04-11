from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from iuem.photorepository.metadatamanager import METADATA_KEY


class MetadataView(BrowserView):
    """a view"""
    
    def metadata(self):
        annotations = IAnnotations(self.context)
        return annotations[METADATA_KEY]