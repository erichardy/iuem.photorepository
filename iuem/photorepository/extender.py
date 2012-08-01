# fields are in Products.Archetypes.Field
# widgets are in Products.Archetypes.Widget
# both are imported by Products.Archetypes.atapi
from Products.Archetypes.atapi import *
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.subtypes.image import ExtensionBlobField
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.ATContentTypes.interface import IATImage , IATFolder
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.AddRemoveWidget import AddRemoveWidget , ComboBoxWidget
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from iuem.photorepository import iuemRepositoryMessageFactory as _

from zope.component import adapts
from zope.interface import implements

from validators import isLatitude , isLongitude

class _ExtensionImageField(ExtensionField, ImageField): pass
class _ExtensionStringField(ExtensionField, StringField): pass
class _ExtensionLinesField(ExtensionField, LinesField): pass
class _ExtensionTextField(ExtensionField, TextField): pass
class _ExtensionDateTimeField(ExtensionField, DateTimeField): pass
class _ExtensionFloatField(ExtensionField, FloatField): pass
class _ExtensionIntegerField(ExtensionField, IntegerField): pass
class _ExtensionBooleanField(ExtensionField, BooleanField): pass
class _ExtensionComputedField(ExtensionField, ComputedField): pass



class FolderImageRepositoryExtender(object):
    adapts(IATFolder)
    implements(ISchemaExtender)

    fields = [
        # Common fields with images
        _ExtensionLinesField (u"general",
            searchable = True,
            multiValued = True,
            isMetadata = True,
            # index_method="generalIndexMethod",
            vocabulary = NamedVocabulary(u"general_voc"),
            default = [],               
            widget = AddRemoveWidget(
                    label=_(u"General keywords"),
                    description = _(u"General keywords"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"science",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"science_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Scientific keywords"),
                    description = _(u"Scientific keywords"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"where",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"localization_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Where"),
                    description = _(u"Area related to the photo"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"laboratory",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"laboratory_voc"),
            default = [],              
            widget = AddRemoveWidget(
                    label=_(u"Laboratory"),
                    description = _(u"Photograph's Laboratory"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"reseachproject",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"researchproj_voc"),
            default = [],              
            widget = AddRemoveWidget(
                    label=_(u"Research Project"),
                    description = _(u"Research Project related to the picture"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"licencetype",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"licencetype_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Licence Type"),
                    description = _(u"What type of restricted usage"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionDateTimeField(u"recording_date_time",
            searchable=True,
            widget=CalendarWidget(
                    label=_(u'Recording date and time'),
                    description=_(u'Recording date and time, may be extracted from XMP, EXIF or IPCT'),
                    ),
            ),
        _ExtensionStringField (u"photographer",
            searchable = True,
            default_method = "Creator",
            widget = StringWidget(
                    label=_(u"Author of the photo"),
                    description = _(u"Who owns this photo"),
                    size = 50,
                    ),
        ),
        _ExtensionImageField(u"watermark",
        widget = ImageWidget(
            label=_(u"Watermark"),
            description=_(u'Image used for watermark'),
            visible={'view': 'invisible', 'edit': 'invisible' },
            ),
        ),
        # Common fields with images
    ]
    def __init__(self, context):
        self.context = context
        
    def generalIndexMethod(self):
        print 'Dans generalIndexMethod'
        fieldName = 'general'
        termUID = self.getField(fieldName).get(self)
        return self.getField(fieldName).vocabulary.getKeyPathForTerms(self, termUID)

    def getFields(self):
        return self.fields
    

class ImageImageRepositoryExtender(object):
    adapts(IATImage)
    implements(ISchemaExtender)

    fields = [
        ExtensionBlobField(u"sourceImage",
        accessor = 'getSourceImage',
        mutator = 'setSourceImage',
        languageIndependent = True,
        widget = ImageWidget(
            label=u"Original hi-res image",
            visible={'view': 'visible', 'edit': 'invisible' }
            ),
        ),
        # Common fields with Folders
        _ExtensionLinesField (u"general",
            searchable = True,
            multiValued = True,
            isMetadata = True,
            vocabulary = NamedVocabulary(u"general_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"General keywords"),
                    description = _(u"General keywords"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"science",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"science_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Scientific keywords"),
                    description = _(u"Scientific keywords"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),                               
        ),
        _ExtensionStringField (u"where",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"localization_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Where"),
                    description = _(u"Area related to the photo"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"laboratory",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"laboratory_voc"),
            default = [],      
            widget = AddRemoveWidget(
                    label=_(u"Laboratory"),
                    description = _(u"Photograph's Laboratory"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"reseachproject",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"researchproj_voc"),
            default = [], 
            widget = AddRemoveWidget(
                    label=_(u"Research Project"),
                    description = _(u"Research Project related to the picture"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField (u"licencetype",
            searchable = True,
            multiValued = True,
            vocabulary = NamedVocabulary(u"licencetype_voc"),
            default = [],
            widget = AddRemoveWidget(
                    label=_(u"Licence Type"),
                    description = _(u"What type of restricted usage"),
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionDateTimeField(u"recording_date_time",
            searchable=True,
            widget=CalendarWidget(
                    label=_(u'Recording date and time'),
                    description=_(u'Recording date and time, may be extracted from XMP, EXIF or IPCT'),
                    ),
            ),
        _ExtensionStringField (u"photographer",
            searchable = True,
            default_method = "Creator",
            widget = StringWidget(
                    label=_(u"Photographer"),
                    description = _(u"Who owns this photo"),
                    size = 50,
                    ),
        ),
        _ExtensionImageField(u"watermark",
        widget = ImageWidget(
            label=_(u"Watermark"),
            description=_(u'Image used for watermark'),
            visible={'view': 'invisible', 'edit': 'invisible' },
            ),
        ),
        # End of common fields with Folders
        _ExtensionStringField(u"latitude",
            searchable = True,
            validators = ('isLatitude',),
            widget = StringWidget(
                label = _(u"Latitude"),
                description=_(u'latitude_format'),
                visible={'view': 'invisible', 'edit': 'invisible' },
                maxlength = 50,
                size = 50
                ),
        ),
        _ExtensionStringField(u"longitude",
            searchable = True,
            validators = ('isLongitude',),
            widget = StringWidget(
                label = u"Longitude",
                description=_(u'longitude_format'),
                visible={'view': 'invisible', 'edit': 'invisible' },
                maxlength = 50,
                size = 50
                ),
        ),
        _ExtensionStringField (u"exif",
            expression = 'self.sourceImage.getEXIF()',
            widget = StringWidget(
                    modes=('view',),                
                    label=_(u'EXIF metadatas'),
                    description=_(u'EXIF metadata in the picture'),
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),
        _ExtensionStringField (u"xmp",
            widget = StringWidget(
                    modes=('view',),           
                    label=_(u'XMP metadata description'),
                    description=_(u'XMP metadata description'),
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),
        _ExtensionStringField (u"ipct",
            widget = StringWidget(
                    modes=('view',),
                    label=_(u'IPCT metadata'),
                    description=_(u'IPCT metadata description'),
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),

    ]
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
    
    def getPhotographer(self):
        return str(self.context.Creators()[0])
    
    def getSourceExif(self):
        return self.fields[12]

class imPhotoSmallImageExtender(object):
    adapts(IATImage)
    implements(ISchemaExtender)

    """part of code from unweb.watermark"""
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

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


    

