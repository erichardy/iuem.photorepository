from iuem.photorepository import iuemMessageFactory as _

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class MetadataConfirmView(BrowserView):
    
    def whereToSpread(self):
        context = self.context
        return context.whereToSpread
    
    def addOrReplace(self):
        context = self.context
        return context.addOrReplace
    
    def description(self):
        context = self.context
        return context.description
    
    def general(self):
        context = self.context
        return context.general
    
    def science(self):
        context = self.context
        return context.science
    
    def where(self):
        context = self.context
        return context.where
    
    def laboratory(self):
        context = self.context
        return context.laboratory
    
    def reseachproject(self):
        context = self.context
        return context.reseachproject
    
    def licencetype(self):
        context = self.context
        return context.licencetype
    
    def recording_date_time(self):
        context = self.context
        return context.recording_date_time
    
    def photographer(self):
        context = self.context
        return context.photographer


class SpreadMetadata(BrowserView):
    
    def __call__(self):
        context = self.context
        request = self.request
        portal = context.portal_url.getPortalObject()
        catalog = getToolByName(portal , 'portal_catalog')
        query = {}
        query['path'] = {'query':'/'.join(context.getPhysicalPath()) , 'depth':1}
        query['portal_type'] = 'Image'
        results = catalog(query)
        # import pdb;pdb.set_trace()
        # http://plone.org/documentation/manual/developer-manual/indexing-and-searching/querying-the-catalog
        for brains in results:
            print brains.getObject().getId()
            print brains.getObject().Description()
            obj = brains.getObject()
            print obj['where']
        # print "in Spread Metadata...."
        # print request.form
        # print '----'
        # print catalog
        # print "\n"
