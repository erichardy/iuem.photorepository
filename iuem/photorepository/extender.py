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
class _ExtensionDateTimeField(ExtensionField, DateTimeField): pass
class _ExtensionLinesField(ExtensionField, LinesField): pass
class _ExtensionComputedField(ExtensionField, ComputedField): pass


class FolderImageRepositoryExtender(object):
    adapts(IATFolder)
    implements(ISchemaExtender)

    fields = [
        _ExtensionStringField ("""where""",
            vocabulary = NamedVocabulary("imlocationvoc"),                   
            widget = SelectionWidget(
                    label=u"Where",
                    description = u"area where the photo is from",
                    ),
        ),
        _ExtensionStringField ("laboratory",
            vocabulary = NamedVocabulary("imteamvoc"),                   
            widget = SelectionWidget(
                    label=u"Laboratory",
                    description = u"Photograph's Laboratory",
                    ),
        ),
        _ExtensionStringField ("reseachproject",
            vocabulary = NamedVocabulary("improjectvoc"),                   
            widget = SelectionWidget(
                    label=u"Reseach Project",
                    description = u"Reseach Project related to the images",
                    ),
        ),

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
            label="Original hi-res image",
            visible={'view': 'visible', 'edit': 'invisible' }
            ),
        ),
        _ExtensionStringField ("""where""",
            vocabulary = NamedVocabulary("imlocationvoc"),
            mutator = "setWhere",                
            widget = AddRemoveWidget(
                    label=u"Where",
                    description = u"Area related to the photo",
                    allow_add = 1,
                    role_based_add = 1,
                    size = 5,
                    ),
        ),
        _ExtensionStringField ("laboratory",
            vocabulary = NamedVocabulary("imteamvoc"),                   
            widget = SelectionWidget(
                    label=u"Laboratory",
                    description = u"Photograph's Laboratory",
                    ),
        ),
        _ExtensionStringField ("reseachproject",
            vocabulary = NamedVocabulary("improjectvoc"),                   
            widget = SelectionWidget(
                    label=u"Reseach Project",
                    description = u"Reseach Project related to the images",
                    ),
        ),
        _ExtensionStringField ("general",
            vocabulary = NamedVocabulary("imtagvoc"),                   
            widget = InAndOutWidget(
                    label=u"Global key word",
                    description = u"Global key word",
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


    

