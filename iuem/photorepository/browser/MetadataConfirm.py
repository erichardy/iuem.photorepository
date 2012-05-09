from iuem.photorepository import iuemMessageFactory as _

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class MetadataConfirmView(BrowserView):
    # import pdb;pdb.set_trace()

    def general(self):
        context = self.context
        return context.general

    def where(self):
        context = self.context
        return context.where


class SpreadMetadata(BrowserView):
    
    def __call__(self):
        context = self.context
        request = self.request
        portal = context.portal_url.getPortalObject()
        catalog = getToolByName(portal , 'portal_catalog')
        # http://plone.org/documentation/manual/developer-manual/indexing-and-searching/querying-the-catalog
        print "in Spread Metadata...."
        print request.form
        print '----'
        print catalog
        print "\n"