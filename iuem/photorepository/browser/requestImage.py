import logging
from Products.Five import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from iuem.photorepository import iuemRepositoryMessageFactory as _
from iuem.photorepository.interfaces import IPhotorepositorySettings

logger = logging.getLogger('iuem.photorepository')

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        return False
        # raise EmailAddressInvalid(value)
    return True


class RequestImage(BrowserView):
    
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


class RequestImageFormResult(BrowserView):
    
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
        fullname          = request['fullname']
        email             = request['email']
        team             = request['team']
        usage_description = request['usage_description']
        urlSourceImage    = request['urlSourceImage'] + '/view'
        try:
            accept_conditions = request['accept_conditions']
        except:
            accept_conditions = False
        request_content = {}
        request_content['fullname'] = fullname
        request_content['email'] = email
        request_content['team'] = team
        request_content['usage_description'] = usage_description
        request_content['urlSourceImage'] = urlSourceImage
        request_content['accept_conditions'] = accept_conditions
        validForm = validateaddress(email)
        validForm = validForm and fullname and team and usage_description
        validForm = validForm and accept_conditions
        if not validForm:
            request_content['sent'] = 'no'
            return request_content
        
        subject = _(u'[IUEM Photo repository] Image request')
        # message = fullname + '\n' + email + '\n' + team + '\n'
        # message = message + usage_description + '\n'
        # message = message + urlSourceImage + '\n'
        message = _(u"Original image request from :\n")
        message += _(u"Name : ") + unicode(fullname,'utf8') + '\n'
        message += _(u"email adress : ") + email + '\n'
        message += _(u"team : ") + unicode(team,'utf-8') + '\n'
        message += _(u"Image usage : ") + unicode(usage_description,'utf-8') + '\n\n'
        message += _(u"Image URL : ") + urlSourceImage
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        mailhost = getToolByName(self.context , 'MailHost')
        mfrom = settings.request_image_from
        for target in settings.request_image_emails:
            mailhost.send(message.encode('utf8') , subject = subject ,\
                          mto = target , mfrom = mfrom , charset='utf8')
        copy_message = _(u"copy-of-message :\n\n") + message
        mailhost.send(copy_message.encode('utf8') , subject = subject ,\
                      mto = email , mfrom = mfrom , charset='utf8')
        request_content['sent'] = 'ok'
        
        return request_content

        


