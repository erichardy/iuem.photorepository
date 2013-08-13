# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema
from z3c.form import field , button
from plone.directives import form

from iuem.photorepository import iuemRepositoryMessageFactory as _

defaultWatermarkConfigValue = u"var config = {\n"
defaultWatermarkConfigValue = defaultWatermarkConfigValue + u'    "position": "bottom-left",\n'
defaultWatermarkConfigValue = defaultWatermarkConfigValue + u'    "opacity": 8,\n'
defaultWatermarkConfigValue = defaultWatermarkConfigValue + u'    "className": "watermark",\n'
defaultWatermarkConfigValue = defaultWatermarkConfigValue + u'    "path": "++resource++iuem_repository_static/img/filigrane.png"\n'
defaultWatermarkConfigValue = defaultWatermarkConfigValue + u'};'

# thanks to
# http://plone.org/documentation/kb/how-to-create-a-plone-control-panel-with-plone.app.registry

class IPhotorepositorySettings(Interface):
    
    request_image_emails = schema.List (
                        title = _(u"email addresses which receive image requests"),
                        description = _(u"request_image_emails_description"),
                        value_type = schema.TextLine(),
                        required = True,
                        default = [],
                        )
    request_image_from = schema.TextLine (
                        title = _(u"From field for original image requests"),
                        description = _(u"enter a valid email adress"),
                        default = u"iuem.photorepository@iuem-photorepository.org",
                        required = True,
                        )
    request_image_url = schema.TextLine (
                        title = _(u"View name of the form for request an image"),
                        description = _(u"TAL expression (@@request-image)"),
                        default = u"@@request-image",
                        required = True,
                        )

    request_album_emails = schema.List (
                        title = _(u"email addresses which receive album requests"),
                        description = _(u"request_album_emails_description"),
                        value_type = schema.TextLine(),
                        required = True,
                        default = [],
                        )
    request_album_from = schema.TextLine (
                        title = _(u"From field for album requests"),
                        description = _(u"enter a valid email adress"),
                        default = u"iuem.photorepository@iuem-photorepository.org",
                        required = True,
                        )
    request_album_url = schema.TextLine (
                        title = _(u"View name of the form for request an access or an album"),
                        description = _(u"TAL expression (string:${absolute_url}/@@request-album)"),
                        default = u"@@request-album",
                        required = True,
                        )
    watermark_config = schema.Text (
                        title = _(u"Javascript code for the configuration of watermark"),
                        description = _(u"Must be a valid Javascript code"),
                        default = defaultWatermarkConfigValue,
                        required = True,
                        )
    watermark_image = schema.Bytes(
                        title = u'Watermark image file',
                        )
    watermark_opacity = schema.Float(title = u'Watermark opacity percentage',
                        min = 0.1, 
                        max = 1.0, 
                        default = 0.15,
                        )
    
# @form.default_value(field=IPhotorepositorySettings['watermark_config'])
    