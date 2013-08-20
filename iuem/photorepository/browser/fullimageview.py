import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone import api
from iuem.photorepository.interfaces import IPhotorepositorySettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from DateTime import DateTime
from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

class fullImageView(BrowserView):
    """full view for image repository
    """
    def duplicate(self):
        context = self.context
        registry = getUtility(IRegistry)
        targetFolder = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.fullimages_folder']
        try:
            target = api.content.get(path = targetFolder)
            # logger.info('Folder for full images found ! (%s)' , targetFolder)
        except:
            logger.info('Folder for full images NOT found ! (%s)' , targetFolder)
            return
        # import pdb;pdb.set_trace()
        try:
            # logger.info('old full image to be deleted (%s)' , context.getId())
            with api.env.adopt_roles(['Manager']):
                # logger.info('.')
                newfull = api.content.get(path = targetFolder + '/' + context.getId())
                # logger.info('..' + newfull.getId())
                target.manage_delObjects([context.getId(),])
                # logger.info('...')
                logger.info('old full image deleted (%s)' , newfull.getId())
        except:
            logger.info('No previous full image deleted...')
        
        with api.env.adopt_roles(['Manager']):
            target.invokeFactory(type_name='Image', id = self.context.getId())
        return
    
    def deleteOldObjects(self , target):
        with api.env.adopt_roles(['Manager']):
            now = DateTime()
            for objId in target.keys():
                # logger.info(target[objId].creation_date)
                # logger.info(objId)
                obj = target[objId]
                # logger.info(obj)
                creationDate = obj.creation_date
                # 0.002 ~ 3 minutes
                if now > (creationDate + 0.002):
                    target.manage_delObjects([objId , ])
                # import pdb;pdb.set_trace()
                
        
    def fullImage(self):
        context = self.context
        registry = getUtility(IRegistry)
        targetFolder = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.fullimages_folder']
        target = api.content.get(path = targetFolder)
        newimage = target[context.getId()]
        """ Security """
        workflowTool = getToolByName(context, "portal_workflow")
        workflowTool.doActionFor(newimage, "retract")
        mt = getToolByName(context, 'portal_membership')
        currentMember = mt.getAuthenticatedMember()
        logger.info('Current User : ' + str(currentMember))
        newimage.changeOwnership(currentMember)
        newimage.manage_setLocalRoles(currentMember , ("Owner",))
        context.reindexObjectSecurity()
        """ Delete old objects """
        self.deleteOldObjects(target)
        source = context.getField("sourceImage")
        newimage.setImage(source.get(context).data)
        newimageId = newimage.getId()
        newimageContainer = newimage.aq_parent
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.redirect(newimageContainer.absolute_url() + '/' + newimageId)
        return RESPONSE.redirect
        
    def header(self):
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Type','image/jpg')
        RESPONSE.setHeader('Content-Disposition' , 'attachment; filename=' + self.context.getId())
        return RESPONSE
