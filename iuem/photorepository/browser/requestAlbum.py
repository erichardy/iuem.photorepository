import logging
from Products.Five import BrowserView

from plone.autoform.form import AutoExtensibleForm
from plone.autoform.view import WidgetsView
from plone.z3cform import layout
from zope import interface
from zope import schema
from z3c.form import form, button, field
from Products.CMFCore.utils import getToolByName

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        return False
        # raise EmailAddressInvalid(value)
    return True

class RequestAlbum(BrowserView):

    def currentUser(self):
        ms = getToolByName(self.context , 'portal_membership')
        member = ms.getAuthenticatedMember()
        currentUser = {}
        currentUser['email'] = member.getProperty('email')
        currentUser['fullname'] = member.getProperty('fullname')
        for k in currentUser.keys():
            if currentUser[k] == None:
                currentUser[k] = ''
        return currentUser

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
        team             = request['team']
        usage_description = request['usage_description']
        urlSourceImage    = request['urlSourceImage'] + '/view'
        subject = _(u'[IUEM Photo repository] Album or access request')
        message = fullname + '\n' + email + '\n' + team + '\n'
        message = message + usage_description + '\n'
        message = message + urlSourceImage + '\n'
        message = _(u"Original image request from :\n")
        message += _(u"Name : ") + fullname + '\n'
        message += _(u"email adress : ") + email + '\n'
        message += _(u"team : ") + team + '\n'
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
        request_content['team'] = team
        request_content['usage_description'] = usage_description
        request_content['urlSourceImage'] = urlSourceImage        
        return request_content

        


