# from iuem.photorepository import iuemMessageFactory as _
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from iuem.photorepository.manageVocabulary import imMetadatas

def strToList(strOrList):
    """ returns a list even if strOrList is a str"""
    toReturn = []
    if isinstance(strOrList , str):
        toReturn.append(strOrList)
        return toReturn
    else:
        return strOrList


class MetadataConfirmView(BrowserView):
    adapts(IATFolder)

    def __call__(self):
        # print self.request.form
        return self.index()

    def wheretospread(self):
        return self.request.form['wheretospread']
    
    def addorreplace(self):
        return self.request.form['addorreplace']
    
    def description(self):
        try:
            return self.request.form['description']
        except:
            return False
    
    def general(self):
        try:
            return strToList(self.request.form['general'])
        except:
            return False
    
    def science(self):
        try:
            return strToList(self.request['science'])
        except:
            return False
    
    def where(self):
        try:
            return strToList(self.request['where'])
        except:
            return False
    
    def laboratory(self):
        try:
            return self.request['laboratory']
        except:
            return False
    
    def reseachproject(self):
        try:
            return strToList(self.request['reseachproject'])
        except:
            return False
    
    def licencetype(self):
        try:
            return strToList(self.request['licencetype'])
        except:
            return False
    
    def recording_date_time(self):
        try:
            return self.request['recording_date_time']
        except:
            return False
    
    def photographer(self):
        try:
            return self.request['photographer']
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
    print obj.photographer
    obj.photographer = form['photographer']
    print obj.photographer
  
    print '------------------------'
    """first, we treat metadata without vocabulary
    description , recording_date_time , photographer
    """
    obj.reindexObject()
    return

