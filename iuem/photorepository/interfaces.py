
from zope.interface import Interface
from zope import schema

from iuem.photorepository import iuemRepositoryMessageFactory as _

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


# thanks to
# http://plone.org/documentation/kb/how-to-create-a-plone-control-panel-with-plone.app.registry


