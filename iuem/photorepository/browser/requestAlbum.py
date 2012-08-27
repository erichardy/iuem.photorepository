import logging
from Products.Five import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from iuem.photorepository.interfaces import IPhotorepositorySettings

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

    def sendRequestAlbumMail(self):
        request           = self.request
        fullname          = request['fullname']
        email             = request['email']
        team              = request['team']
        access_type       = request['access_type']
        new_album_name    = request['new_album_name']
        usage_description = request['usage_description']
        album              = request['album']
        request_content = {}
        validForm = validateaddress(email)
        validForm = validForm and fullname and team
        if (access_type=="New album request"):
            validForm = validForm and new_album_name and usage_description
        request_content['fullname'] = fullname
        request_content['email'] = email
        request_content['team'] = team
        request_content['usage_description'] = usage_description
        request_content['access_type'] = access_type
        request_content['new_album_name'] = new_album_name
        request_content['album'] = album

        if not validForm:
            request_content['sent'] = 'no'
            return request_content
        
        request_content['sent'] = 'ok'
        subject = _(u'[IUEM Photo repository] Album or access request')
        message = fullname + '\n' + email + '\n' + team + '\n'
        message = message + usage_description + '\n'
        message = message + '\n'
        message = _(u"Your request : ") + _(access_type) + '\n'
        message += _(u"Name : ") + fullname + '\n'
        message += _(u"email adress : ") + email + '\n'
        message += _(u"team : ") + team + '\n'
        message += _(u"full album URL : ") + album + '/' + new_album_name + '\n'
        message += _(u"album usage : ") + usage_description + '\n\n'
        
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        mailhost = getToolByName(self.context , 'MailHost')
        mfrom = settings.request_album_from
        for target in settings.request_album_emails:
            mailhost.send(message , subject = subject ,\
                          mto = target , mfrom = mfrom)
        copy_message = _(u"copy-of-message :\n\n") + message
        mailhost.send(copy_message , subject = subject ,\
                      mto = email , mfrom = mfrom)
        
        return request_content
