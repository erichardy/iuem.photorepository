import logging
from Products.Five import BrowserView

from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout

from zope import interface
from zope import schema
from z3c.form import form, button, field


from Products.CMFCore.utils import getToolByName

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

#http://plone.org/documentation/kb/easy-forms-with-plone3

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        return False
        # raise EmailAddressInvalid(value)
    return True

class IRequestAlbum(interface.Interface):
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
    
    
class RequestAlbum(AutoExtensibleForm , form.Form):
    # grok.name('query-image')
    # grok.require('zope2.View')
    # grok.context(IATImage)
    schema = IRequestAlbum
    ignoreContext = True
    
    label = u"Query an Image"
    descrition = u"this form is used to query an image to the owner"
    # import pdb;pdb.set_trace()
    """
    def getContent(self):
        data = {}
        data['name'] = 'Mon nom a moi'
        data['email'] = 'eric.hhh@tre.fr'
        data['urlSourceImage'] = 'http://url.oftheImage.fr'
        logger.info('in getContent: ' + str(self.request.HTTP_REFERER))
        # import pdb;pdb.set_trace()
        return data
    """
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

class RequestAlbumView(layout.FormWrapper):
    label = u"The form wrapper"
    form = RequestAlbum



"""
class IRequestAlbum(interface.Interface):
    fullname = schema.TextLine (
            title = _(u"fullname"),
            )
    email = schema.TextLine(
            title = _(u"email"),
            )
    unity = schema.TextLine  (
            title = _(u"unity"),
            )

class RequestAlbum(AutoExtensibleForm , form.Form):

    fields = field.Fields(IRequestAlbum)
    label = _(u"request album")
    description = _(u"request album description")
    ingnoreContext = True

    @button.buttonAndHandler(_(u'Send Request'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.forErrorMessage
            return

class RequestAlbumView(layout.FormWrapper):
    label = u"The form wrapper"
    form = RequestAlbum
"""
class RequestAlbumFormResult(BrowserView):
    
    def sendRequest(self):
        request = self.request
        return
    
    def getMailAddr(self):
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        for m in settings.request_image_emails:
            logger.info(m)

    def sendRequestImageMail(self):
        request           = self.request
        email             = request['email']
        if not validateaddress(email):
            msg = _(u"Sorry, your email adress is invalid, the request can't be satisfied...")
            return msg
        fullname          = request['fullname']
        unity             = request['unity']
        usage_description = request['usage_description']
        urlSourceImage    = request['urlSourceImage'] + '/view'
        subject = _(u'[IUEM Photo repository] Image request')
        message = fullname + '\n' + email + '\n' + unity + '\n'
        message = message + usage_description + '\n'
        message = message + urlSourceImage + '\n'
        message = _(u"Original image request from :\n")
        message += _(u"Name : ") + fullname + '\n'
        message += _(u"email adress : ") + email + '\n'
        message += _(u"Unity : ") + unity + '\n'
        message += _(u"Image usage : ") + usage_description + '\n\n'
        message += _(u"Image URL : ") + urlSourceImage
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        mailhost = getToolByName(self.context , 'MailHost')
        mfrom = settings.request_image_from
        for target in settings.request_image_emails:
            mailhost.send(message , subject = subject ,\
                          mto = target , mfrom = mfrom)
        copy_message = _(u"copy-of-message :\n\n") + message
        mailhost.send(copy_message , subject = subject ,\
                      mto = email , mfrom = mfrom)
        request_content = {}
        request_content['fullname'] = fullname
        request_content['email'] = email
        request_content['unity'] = unity
        request_content['usage_description'] = usage_description
        request_content['urlSourceImage'] = urlSourceImage        
        return request_content

        


