from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iuem.photorepository.manageVocabulary import imMetadatas
from AccessControl import getSecurityManager
from iuem.photorepository import iuemRepositoryMessageFactory as _

class repoImageView(BrowserView):
    """new view for image repository
    """

    def sourceImage(self):
        context = self.context
        """
        tag = '<img src="' + context.absolute_url() + '/sourceImage" '
        tag += 'ALT="' + str(context.title) + '" '
        tag += 'title="' + str(context.title) + '" '
        tag += 'height="' + str(context.sourceImage.height) + '" '
        tag += 'width="' + str(context.sourceImage.width) + '" '
        tag += '/>'
        """
        tag = context.absolute_url() + '/sourceImage'
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
        return str(self.context.photographer)

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
    
    def canViewFullImage(self):
        sm = getSecurityManager()
        if sm.checkPermission("iuem.photorepository: View Full Image" , self.context):
            return True
        else:
            return False
        