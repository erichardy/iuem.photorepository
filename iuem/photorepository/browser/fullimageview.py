import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iuem.photorepository.manageVocabulary import imMetadatas
from AccessControl import getSecurityManager
from iuem.photorepository.interfaces import IPhotorepositorySettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

class fullImageView(BrowserView):
    """full view for image repository
    """
    
    """
    def __call__(self):
        # import pdb;pdb.set_trace()
        context = self.context
    """
    
    def coucou(self):
        # import pdb;pdb.set_trace()
        # REQUEST = self.REQUEST
        return 'coucou'
    
    def header(self):
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Type','image/jpg')
        RESPONSE.setHeader('Content-Disposition' , 'attachment; filename=' + self.context.getId())
        return RESPONSE
