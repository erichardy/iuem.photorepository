from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from iuem.photorepository.manageVocabulary import imMetadatas
from iuem.photorepository.extender import ImageImageRepositoryExtender
from iuem.photorepository.extender import FolderImageRepositoryExtender



"""
Fill in vocabularies for testing purpose
"""

class fillInVocabularies(BrowserView):
    """ 
    """
    def __call__(self):
        # general_voc science_voc localization_voc laboratory_voc researchproj_voc licencetype_voc
        return self.index()
    
    def vocabs(self):
        context = self.context
        vocabs = getToolByName(context , 'portal_vocabularies')
        for voc in vocabs:
            print voc
        vocabs['general_voc'].addTerm(key='lacle' , value = u'La cle' , termtype='SimpleVocabularyTerm',silentignore=True)
        # import pdb;pdb.set_trace()