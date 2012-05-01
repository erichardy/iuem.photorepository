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

from zope.component import adapts
from zope.interface import implements

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
        _ExtensionLinesField (u"where",
            searchable = True,                               
            vocabulary = NamedVocabulary("imlocationvoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Where",
                    description = u"Area related to the photo",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("laboratory",
            searchable = True,
            vocabulary = NamedVocabulary("imteamvoc"),
            default = [],              
            widget = AddRemoveWidget(
                    label=u"Laboratory",
                    description = u"Photograph's Laboratory",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("reseachproject",
            searchable = True,
            vocabulary = NamedVocabulary("improjectvoc"),
            default = [],              
            widget = AddRemoveWidget(
                    label=u"Reseach Project",
                    description = u"Reseach Project related to the images",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("general",
            searchable = True,
            vocabulary = NamedVocabulary("imtagvoc"),
            default = [],               
            widget = AddRemoveWidget(
                    label=u"Global key word",
                    description = u"Global key word",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("science",
            searchable = True,
            vocabulary = NamedVocabulary("imscitagvoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Scientific key word",
                    description = u"Scientific key word",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("licencetype",
            searchable = True,
            vocabulary = NamedVocabulary("imlicencevoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Licence Type",
                    description = u"What type of restricted usage",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionDateTimeField("""date_and_time""",
            searchable=True,
            widget=CalendarWidget(
                    label=u'Recording date and time',
                    description=u'Recording date and time, may be extracted from XMP, EXIF or IPCT',
                    ),
            ),
        _ExtensionStringField ("author",
            searchable = True,
            widget = StringWidget(
                    label=u"Author of the photo",
                    description = u"Who owns this photo",
                    size = 50,
                    ),
        ),
        ExtensionBlobField("watermark",
        widget = ImageWidget(
            label=u"Watermark",
            visible={'view': 'invisible', 'edit': 'visible' }
            ),
        ),
        # Common fields with images
    ]
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
    

class ImageImageRepositoryExtender(object):
    adapts(IATImage)
    implements(ISchemaExtender)

    fields = [
        ExtensionBlobField("original",
        accessor = 'getOriginal',
        mutator = 'setOriginal',
        languageIndependent = True,
        widget = ImageWidget(
            label=u"Original hi-res image",
            visible={'view': 'visible', 'edit': 'invisible' }
            ),
        ),
        # Common fields with Folders
        _ExtensionStringField ("""where""",
            searchable = True,                               
            vocabulary = NamedVocabulary("imlocationvoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Where",
                    description = u"Area related to the photo",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("laboratory",
            searchable = True,
            vocabulary = NamedVocabulary("imteamvoc"),
            default = [],      
            widget = AddRemoveWidget(
                    label=u"Laboratory",
                    description = u"Photograph's Laboratory",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("reseachproject",
            searchable = True,
            vocabulary = NamedVocabulary("improjectvoc"),
            default = [], 
            widget = AddRemoveWidget(
                    label=u"Reseach Project",
                    description = u"Reseach Project related to the images",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("general",
            searchable = True,
            vocabulary = NamedVocabulary("imtagvoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Global key word",
                    description = u"Global key word",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("science",
            searchable = True,
            vocabulary = NamedVocabulary("imscitagvoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Scientific key word",
                    description = u"Scientific key word",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),                               
        ),
        _ExtensionStringField ("licencetype",
            searchable = True,
            vocabulary = NamedVocabulary("imlicencevoc"),
            default = [],
            widget = AddRemoveWidget(
                    label=u"Licence Type",
                    description = u"What type of restricted usage",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionDateTimeField("""date_and_time""",
            searchable=True,
            widget=CalendarWidget(
                    label=u'Recording date and time',
                    description=u'Recording date and time, may be extracted from XMP, EXIF or IPCT',
                    ),
            ),
        _ExtensionStringField ("author",
            searchable = True,
            widget = StringWidget(
                    label=u"Author of the photo",
                    description = u"Who owns this photo",
                    size = 50,
                    ),
        ),
        ExtensionBlobField("watermark",
        widget = ImageWidget(
            label=u"Watermark",
            visible={'view': 'invisible', 'edit': 'visible' }
            ),
        ),
        # End of common fields with Folders
        _ExtensionComputedField ("exif",
            widget = ComputedWidget(
                    modes=('view',),                
                    label=u'EXIF metadata',
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),
        _ExtensionComputedField ("xmp",
            widget = ComputedWidget(
                    modes=('view',),           
                    label=u'XMP metadata',
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),
        _ExtensionComputedField ("ipct",
            widget = ComputedWidget(
                    modes=('view',),
                    label=u'IPCT metadata',
                    visible={'view': 'visible', 'edit': 'hidden' },
                    ),
        ),

    ]
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
    

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


    

