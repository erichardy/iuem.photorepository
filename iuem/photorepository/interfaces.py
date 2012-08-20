
from zope.interface import Interface
from zope import schema

from iuem.photorepository import iuemRepositoryMessageFactory as _

class IPhotorepositorySettings(Interface):
    
    query_image_emails = schema.List (
                        title = _(u"email addresses which receive image queries"),
                        description = _(u"query_image_emails_description"),
                        value_type = schema.TextLine(),
                        required = False,
                        default = [],
                        )
    query_album_emails = schema.List (
                        title = _(u"email addresses which receive album queries"),
                        description = _(u"query_album_emails_description"),
                        value_type = schema.TextLine(),
                        required = False,
                        default = [],
                        )

# thanks to
# http://plone.org/documentation/kb/how-to-create-a-plone-control-panel-with-plone.app.registry    