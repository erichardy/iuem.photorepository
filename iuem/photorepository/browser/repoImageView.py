import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iuem.photorepository.manageVocabulary import imMetadatas
from AccessControl import getSecurityManager
from iuem.photorepository.interfaces import IPhotorepositorySettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from iuem.photorepository import iuemRepositoryMessageFactory as _

logger = logging.getLogger('iuem.photorepository')

class repoImageView(BrowserView):
    """new view for image repository
    """
    def canViewFullImage(self):
        sm = getSecurityManager()
        if sm.checkPermission("iuem.photorepository: View Full Image" , self.context):
            return True
        else:
            return False
        
    def fullImage(self):
        # logger.info('in sourceImage...')
        context = self.context
        if self.canViewFullImage():
            tag = context.absolute_url() + '/sourceImage'
        else:
            tag = context.absolute_url() + '/view'
        return tag
    
    def originalHeight(self):
        context = self.context
        return str(context.sourceImage.height)
    
    def originalWidth(self):
        context = self.context
        return str(context.sourceImage.width)
    
    def originalType(self):
        context = self.context
        return str(context.sourceImage.content_type)
    
    def viewImage(self):
        return self.context.tag()
    
    def description(self):
        return str(self.context.Description())

    def general(self):
        return self.metadataValues('general')

    def science(self):
        return self.metadataValues('science')
    
    def where(self):
        return self.metadataValues('where')
    
    def laboratory(self):
        return self.metadataValues('laboratory')
    
    def reseachproject(self):
        return self.metadataValues('reseachproject')
    
    def licencetype(self):
        return self.metadataValues('licencetype')
    
    def recording_date_time(self):
        return str(self.context.recording_date_time)
    
    def photographer(self):
        if self.context.photographer == '':
            return ''
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        vocab = myVocabsTool['photographer_voc']
        vocab.getVocabularyDict()[self.context.photographer]
        return str(vocab.getVocabularyDict()[self.context.photographer])

    def sourceExif(self):
        try:
            return eval(str(self.context.exif))
        except:
            return False
    def metadataValues(self , field):
        Kmetadatas = eval(str(self.context[field]))
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        vocab = myVocabsTool[imMetadatas.vocabMetadata[field]]
        metadatas = []
        # import pdb;pdb.set_trace()
        for k in Kmetadatas:
            metadatas.append(vocab.getVocabularyDict()[k])
        return metadatas
    
    def requestImageURL(self):
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IPhotorepositorySettings)
        return settings.request_image_url