# from iuem.photorepository import iuemMessageFactory as _
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from iuem.photorepository.manageVocabulary import imMetadatas



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
        currentFolder = context.absolute_url()
        whereToSpread = request.form['wheretospread']
        addOrReplace = request.form['addorreplace']
        portal = context.portal_url.getPortalObject()
        catalog = getToolByName(portal , 'portal_catalog')
        query = {}
        query['path'] = {'query':'/'.join(context.getPhysicalPath()) , 'depth':9}
        query['portal_type'] = ('Image' , 'Folder')
        
        if whereToSpread == 'Only Local Images':
            query['path'] = {'query':'/'.join(context.getPhysicalPath()) , 'depth':1}
            query['portal_type'] = ('Image')
        results = catalog(query)
        # import pdb;pdb.set_trace()
        # http://plone.org/documentation/manual/developer-manual/indexing-and-searching/querying-the-catalog
        for brains in results:
            if brains.getObject().absolute_url() != currentFolder:
                print str(brains.getObject().getId()) + ' ' + str(brains.getObject().absolute_url())
                obj = brains.getObject()
                updateMetadata(obj , request.form , context)
        nextUrl = self.context.absolute_url()
        for k in request.form.keys():
            print k + ' ' + request.form[k]
        request.response.redirect(nextUrl)
    
def updateMetadata(obj , form , context):
    vocabs = getToolByName(context , 'portal_vocabularies')
    print '------------------------'
    print 'in updateMetadata...'
    print obj.absolute_url()
    print form
    print vocabs
    print '------------------------'
    """first, we treat metadata without vocabulary
    description , recording_date_time , photographer
    BUT, there is a bug : no valid values for recording_date_time and photographer in the request.form
    """
     
