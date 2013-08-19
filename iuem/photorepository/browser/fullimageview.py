import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone import api
from iuem.photorepository.manageVocabulary import imMetadatas
from AccessControl import getSecurityManager
from iuem.photorepository.interfaces import IPhotorepositorySettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from iuem.photorepository import iuemRepositoryMessageFactory as _
import imp

logger = logging.getLogger('iuem.photorepository')

class fullImageView(BrowserView):
    """full view for image repository
    """
    def duplique(self):
        context = self.context
        # import pdb;pdb.set_trace()
        registry = getUtility(IRegistry)
        targetFolder = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.fullimages_folder']
        try:
            target = api.content.get(path = targetFolder)
            tId = target.getId()
            logger.info('Folder for full images found ! (%s)' , targetFolder)
        except:
            logger.info('Folder for full images NOT found ! (%s)' , targetFolder)
            return
        # import pdb;pdb.set_trace()
        try:
            newfull = api.content.get(path = targetFolder + '/' + context.getId())
            api.content.delete(obj = newfull)
            logger.info('old full image deleted (%s)' , newfull.getId())
        except:
            pass
        newimage = api.content.copy(source = context, target = target , safe_id = False)
        # import pdb;pdb.set_trace()
        # RESPONSE = self.context.REQUEST.RESPONSE
        # RESPONSE.redirect(newimage.absolute_url())
        # return RESPONSE.redirect
    
    def redirect(self):
        # import pdb;pdb.set_trace()
        context = self.context
        registry = getUtility(IRegistry)
        targetFolder = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.fullimages_folder']
        newimage = api.content.get(targetFolder + '/' + context.getId())
        newimageId = newimage.getId()
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.redirect(newimage.absolute_url())
        return RESPONSE.redirect
        
        
    def header(self):
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Type','image/jpg')
        RESPONSE.setHeader('Content-Disposition' , 'attachment; filename=' + self.context.getId())
        return RESPONSE
