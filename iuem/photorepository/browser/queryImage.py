import logging
from Products.Five import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

# from Products.CMFCore.interfaces import ISiteRoot
from Products.ATContentTypes.interface import IATImage

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from iuem.photorepository import iuemRepositoryMessageFactory as _
from iuem.photorepository.interfaces import IPhotorepositorySettings

logger = logging.getLogger('iuem.photorepository')

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise EmailAddressInvalid(value)
    return True


class QueryImage(BrowserView):
    
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


class QueryImageFormResult(BrowserView):
    
    def sendQuery(self):
        request = self.request
        """
        logger.info("---------------")
        for k in request.keys():
            logger.info(str(k) + ':' + str(request[k]))
        logger.info("---------------")
        """
        return
    
    def getMailAddr(self):
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        for m in settings.query_image_emails:
            logger.info(m)
        


