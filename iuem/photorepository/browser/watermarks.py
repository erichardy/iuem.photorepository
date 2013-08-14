from iuem.photorepository import iuemRepositoryMessageFactory as _
from iuem.photorepository.subscribers import doThumbnail
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('iuem.photorepository')

class watermarks(BrowserView):
    """ Must be done in a Folder"""
    def __call__(self):
        context = self.context
        if context.portal_type != 'Folder':
            return False
        portal = context.portal_url.getPortalObject()
        catalog = getToolByName(portal , 'portal_catalog')
        logger.info("in restore watermarks...")
        query = {}
        query['path'] = {'query':'/'.join(context.getPhysicalPath()) , 'depth':9}
        query['portal_type'] = ('Image')
        results = catalog(query)
        for brains in results:
            obj = brains.getObject()
            title = obj.getField('title')
            logger.info(title.get(obj))
            if obj.getField('title').get(obj)[:3] != '00-':
                sourceImage = obj.getField("sourceImage").get(obj)
                obj.setImage(sourceImage)
                doThumbnail(obj)

class watermark(BrowserView):
    def __call__(self):
        context = self.context
        if context.portal_type != 'Image':
            return False
        doThumbnail(context)

class full(BrowserView):
    def __call__(self):
        context = self.context
        if context.portal_type != 'Image':
            return
        source = context.getField("sourceImage")
        context.setImage(source.get(context).data)
