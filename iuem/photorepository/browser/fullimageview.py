import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone import api
from iuem.photorepository.interfaces import IPhotorepositorySettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from DateTime import DateTime
from zope.component.hooks import getSite
from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

class fullImageView(BrowserView):
    """full view for image repository
    """
    def duplicate(self):
        context = self.context
        REQUEST = context.REQUEST
        # Copy context object in clipboard
        parent = context.aq_inner.aq_parent
        parent.manage_copyObjects(context.getId(), REQUEST)
        # Find target forlder
        registry = getUtility(IRegistry)
        targetFolder = registry['iuem.photorepository.interfaces.IPhotorepositorySettings.fullimages_folder'] 
        try:
            site = getSite()
            target = site[targetFolder]
            logger.info('Folder for full images found : (%s)' , str(target))
        except:
            logger.info('Folder for full images NOT found ! (%s)' , targetFolder)
            return
        # import pdb;pdb.set_trace()
        # delete object with same id if exist in target folder
        try:
            with api.env.adopt_roles(roles=['Manager']):
                newfull = target[context.getId()]
                target.manage_delObjects([context.getId(),])
                logger.info('old full image deleted (%s)' , newfull.getId())
        except:
            logger.info('No previous full image deleted...')
        
        with api.env.adopt_roles(roles=['Manager']):
            # target.invokeFactory(type_name='Image', id = self.context.getId())
            if context.cb_dataValid():
                try:
                    # Delete old objects
                    self.deleteOldObjects(target)
                    #
                    target.manage_pasteObjects(context.REQUEST['__cp'])
                    newimage = target[context.getId()]
                    # operations on new image
                    self.setNewSecurity(newimage)
                    self.fullImage(newimage)
                    # redirect browser to full image
                    newimageId = newimage.getId()
                    newimageContainer = newimage.aq_parent
                    RESPONSE = self.context.REQUEST.RESPONSE
                    RESPONSE.redirect(newimageContainer.absolute_url() + '/' + newimageId)
                    return RESPONSE.redirect
                except:
                    logger.exception('Exception during pasting in target folder')
                    logger.info('WARNING ! : Object no pasted... : ' + str(context.getId()))
        return
    
    def setNewSecurity(self , newimage):
        """ Security : set owner to object and do it private """
        context = self.context
        workflowTool = getToolByName(context, "portal_workflow")
        workflowTool.doActionFor(newimage, "retract")
        mt = getToolByName(context, 'portal_membership')
        currentMember = mt.getAuthenticatedMember()
        logger.info('Current User : ' + str(currentMember))
        newimage.changeOwnership(currentMember)
        newimage.manage_setLocalRoles(currentMember , ["Owner",])
        return
    
    def deleteOldObjects(self , target):
        """ delete objects older than 3 mn in target """
        with api.env.adopt_roles(['Manager']):
            now = DateTime()
            for objId in target.keys():
                obj = target[objId]
                creationDate = obj.creation_date
                # 0.002 ~ 3 minutes
                if now > (creationDate + 0.002):
                    target.manage_delObjects([objId , ])
                # import pdb;pdb.set_trace()
                
        
    def fullImage(self, newimage):
        context = self.context
        # set image field with full/source image 
        source = context.getField("sourceImage")
        newimage.setImage(source.get(context).data)
        
    def header(self):
        RESPONSE = self.context.REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Type','image/jpg')
        RESPONSE.setHeader('Content-Disposition' , 'attachment; filename=' + self.context.getId())
        return RESPONSE
