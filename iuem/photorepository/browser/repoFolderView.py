from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iuem.photorepository.manageVocabulary import imMetadatas

class repoFolderAlbumView(BrowserView):
    """customization of atct_album_view
    """
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
    
    def metadataValues(self , field):
        Kmetadatas = eval(str(self.context[field]))
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        vocab = myVocabsTool[imMetadatas.vocabMetadata[field]]
        metadatas = []
        # import pdb;pdb.set_trace()
        for k in Kmetadatas:
            metadatas.append(vocab.getVocabularyDict()[k])
        return metadatas
