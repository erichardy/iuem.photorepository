# from iuem.photorepository import iuemMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts



class MetadataConfirmView(BrowserView):
    adapts(IATFolder)

    def __call__(self):
        # print self.request.form
        return self.index()

    def wheretospread(self):
        return self.request.form['form.widgets.wheretospread'][0]
    
    def addorreplace(self):
        return self.request.form['form.widgets.addorreplace'][0]
    
    def description(self):
        try:
            desc = self.request.form['form.widgets.description'][0]
            return self.context[desc]
        except:
            return False
    
    def general(self):
        try:
            return self.request.form['form.widgets.general']
        except:
            return False
    
    def science(self):
        try:
            return self.request.form['form.widgets.science']
        except:
            return False
    
    def where(self):
        try:
            return self.request.form['form.widgets.where']
        except:
            return False
    
    def laboratory(self):
        try:
            return self.request.form['form.widgets.laboratory']
        except:
            return False
    
    def reseachproject(self):
        try:
            return self.request.form['form.widgets.reseachproject']
        except:
            return False
    
    def licencetype(self):
        try:
            return self.request.form['form.widgets.licencetype']
        except:
            return False
    
    def recording_date_time(self):
        try:
            rec = self.request.form['form.widgets.recording_date_time'][0]
            return self.context[rec]
        except:
            return False
    
    def photographer(self):
        try:
            phot = self.request.form['form.widgets.photographer'][0]
            return self.context[phot]
        except:
            return False
    
    def getVocabValue(self, vocabulary , tokken):
        """ return the mapped value of tokken extracted from the vocabulary""" 
        vocabs = getToolByName(self.context,'portal_vocabularies')
        try:
            vocab = vocabs[vocabulary]
        except:
            return False
        try:
            return vocab[tokken].title
        except:
            return False
        

class SpreadMetadata(BrowserView):
    
    def __call__(self):
        # import pdb;pdb.set_trace()
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
        request = self.request
        nextUrl = self.context.absolute_url()
        request.response.redirect(nextUrl)
