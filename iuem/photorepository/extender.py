from Products.Archetypes.public import ImageField, ImageWidget, StringField, StringWidget
from Products.ATContentTypes.interface import IATImage
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.subtypes.image import ExtensionBlobField
from Products.Archetypes.public import ImageWidget, ComputedField
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implements

class _ExtensionImageField(ExtensionField, ImageField):
    pass

class ExtendedComputedField(ExtensionField, ComputedField):
    """ """
    def getFileSize(self, obj):
        return ImageExtender(obj).fields[0].get_size(obj) or 0L
 
    def getImageSize(self,obj):
        try:
            return ImageExtender(obj).fields[0].getSize(obj)
        except:
            return (0,0)


class imPhotoSmallImageExtender(object):
    adapts(IATImage)
    implements(ISchemaExtender)

    """code tire de unweb.watermark"""
    fields = [
        ExtensionBlobField("original",
        accessor = 'getOriginal',
        mutator = 'setOriginal',
        languageIndependent = True,
        widget = ImageWidget(
            label="Original hi-res image",
            visible={'view': 'visible', 'edit': 'invisible' }
            ),
        ),
        ]


    """
    inspire des exemples des docs sur schemaextender
        fields = [
            _ExtensionImageField(
                "Original",
                    widget = ImageWidget(
                    label=u"Small Image",
                    description=u"Image for private view",
                ),
            ),
        ]
    """    
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


    

