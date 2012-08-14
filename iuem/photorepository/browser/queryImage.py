import logging
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout

from zope import interface
from zope import schema
from z3c.form import form, button, field

from Products.CMFCore.interfaces import ISiteRoot
from Products.ATContentTypes.interface import IATImage

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise EmailAddressInvalid(value)
    return True


class IQueryImage(interface.Interface):
    name = schema.TextLine (
                title = _(u"Name and Firstname"),
                description = _(u"Please enter your name and your firstname"),
                required = True
                )
    email = schema.TextLine (
                title = _(u"Your email address"),
                description = _(u"We need your email address to contact you later"),
                constraint = validateaddress,
                required = True
                )
    urlSourceImage = schema.TextLine (
                title = _(u"url"),
                description = _(u"The URL of the Image"),
                required = True
                )
    
    
class QueryImage(AutoExtensibleForm , form.Form):
    # grok.name('query-image')
    # grok.require('zope2.View')
    # grok.context(IATImage)
    schema = IQueryImage
    ignoreContext = True
    
    label = u"Query an Image"
    descrition = u"this form is used to query an image to the owner"
    # import pdb;pdb.set_trace()
    
    def getContent(self):
        data = {}
        data['name'] = 'Mon nom a moi'
        data['email'] = 'eric.hhh@tre.fr'
        data['urlSourceImage'] = 'http://url.oftheImage.fr'
        logger.info('in getContent: ' + str(self.request.HTTP_REFERER))
        # import pdb;pdb.set_trace()
        return data

    @button.buttonAndHandler(u'Ok...')
    def handleOk(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        request = self.request
        # nextUrl = '%s/@@metadata_view_pt'%self.context.absolute_url()
        nextUrl = self.request.HTTP_REFERER
        request.response.redirect(nextUrl)

class QueryImageView(layout.FormWrapper):
    label = u"The form wrapper"
    form = QueryImage









"""
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Text

from z3c.form import field , form
from zope.component import adapts
from Products.ATContentTypes.interface import IATImage

# from plone.directives import form


class IqueryImage(Interface):
    text = Text(
                title = u"Preesentation Text",
                description = u"preesentation Description",
                required = True
                )
    
class queryImage(form.Form):
    adapts(IATImage)
    implements(IqueryImage)
    fields = field.Fields(IqueryImage)
    label = u"le label de queyImage"
    ingnorecontext = True
"""