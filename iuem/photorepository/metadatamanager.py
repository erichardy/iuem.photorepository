from zope import interface
from zope import component
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations

METADATA_KEY = 'IUEM_PHOTOREPOSITORY_METADATA'

class IMetadaManager(interface.Interface):
    """
    metadata manager.... to read and write metadata
    to any plone content
    """
    def read():
        """return the metadata"""
        
    def write(metadata):
        """write the metadata"""

class AnnotationMetadaManager():
    interface.implements(IMetadaManager)
    component.adapts(IAttributeAnnotatable)
    
    def __init__(self , context):
        self.context = context
    
    def read(self):
        annotations = IAnnotations(self.context)
        return annotations[METADATA_KEY]
    
    def write(self , data):
        annotations = IAnnotations(self.context)
        # data['ptype']
        # data['autor']
        new_dict = {}
        for k in data.keys():
            new_dict[k] = data[k]

        annotations[METADATA_KEY] = new_dict
