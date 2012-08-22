from iuem.photorepository import iuemRepositoryMessageFactory as _

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from iuem.photorepository.manageVocabulary import imMetadatas
from iuem.photorepository.extender import ImageImageRepositoryExtender
from iuem.photorepository.extender import FolderImageRepositoryExtender

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
    
    def kwValue(self , kw):
        request = self.request
        form = request.form
        if kw in form.keys():
            if kw in ['description','recording_date_time','photographer']:
                return form[kw]
            else:
                return strToList(form[kw])
        else:
            return False

    def value_of (self , value , vocabulary):
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        try:
            vocab = myVocabsTool[vocabulary]
            return vocab.getVocabularyDict()[value]
        except:
            return ''

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
        # http://plone.org/documentation/manual/developer-manual/indexing-and-searching/querying-the-catalog
        for brains in results:
            if brains.getObject().absolute_url() != currentFolder:
                # print str(brains.getObject().getId()) + ' ' + str(brains.getObject().absolute_url())
                obj = brains.getObject()
                updateMetadata(obj , request.form , context)
        nextUrl = self.context.absolute_url()
        request.response.redirect(nextUrl)
    
def updateMetadata(obj , form , context):
    # vocabs = getToolByName(context , 'portal_vocabularies')
    commonMetadatas = imMetadatas().commonMetadatas
    # if request.form['addorreplace'] == 'Replace metadatas'
    # we cleanup all the fields before to set new values
    if form['addorreplace'] == 'Replace metadatas':
        for k in commonMetadatas:
            # field = nbField(obj,k)
            stringFields = ['recording_date_time','photographer']
            emptyString = ''
            emptyList = []
            if k == 'description':
                obj.setDescription(emptyString)
            elif k in stringFields:
                obj.getField(k).set(obj, emptyString)
            else:
                obj.getField(k).set(obj, emptyList)

    for k in form.keys():
        if k in commonMetadatas:
            if k == 'description':
                obj.setDescription(form[k])
                # import pdb;pdb.set_trace()
            elif k in ['recording_date_time','photographer']:
                # we always replace non vocabulary values                
                obj.getField(k).set(obj, form[k])
            else:
                # field = nbField(obj,k)
                if form['addorreplace'] == 'Add metadatas':
                    # form[k] = values to spread
                    # obj[k] = metadatas values already set to obj
                    lform = list(obj[k])
                    for data in eval(form[k]):
                        if not data in lform:
                            # import pdb;pdb.set_trace()
                            lform.append(data)
                    obj.getField(k).set(obj, lform)
                else:
                    obj.getField(k).set(obj, eval(form[k]))        
    obj.reindexObject()
    return

