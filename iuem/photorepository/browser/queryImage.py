import logging
from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

# from Products.CMFCore.interfaces import ISiteRoot
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
        print request['email']
        print request['fullname']
        print request['unity']
        print request['usage_description']
        print request['urlSourceImage']
        return