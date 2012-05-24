# -*- coding: utf-8 -*-
"""
Various tools to manage iuem.photorepository vocabularies
"""
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager import NamedVocabulary
from zope.app.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary

from Products.Five import BrowserView
from zope.interface import Interface , implements

def defineImVocs(self):
    imVocs = {}
    imVocs['imtypevoc'] = (('type1', u'jpeg'), ('type2', u'tiff'), ('type3', u'png'),('type4', u'gif'),('type5', u'psd'), )
    # imVocs['imtypevoc'] = [] or {} ???...
    imVocs['imlocationvoc'] = (('loc1,',u'Brest'),('loc2,',u'Plouzané'),('loc3,',u'Golf de Gascogne'), )
    # imVocs['imlocationvoc'] = []
    imVocs['imtagvoc'] = (('tag1', u'Mer'), ('tag2', u'Navire'), )
    # imVocs['imtagvoc'] = []
    imVocs['imscitagvoc'] = (('scitag1', u'ADCP'), ('scitag2', u'Mouillage'), )
    # imVocs['imscitagvoc'] = []
    imVocs['imteamvoc'] = (('team1', u'LEMAR'), ('team2', u'Domaine Océanique'), ('team3', u'LMEE'),('team4', u'LPO'))
    # imVocs['imteamvoc'] = []
    imVocs['improjectvoc'] = (('camp1', u'Aspex'), ('camp2', u'Fromvar'), )
    # imVocs['improjectvoc'] = []
    imVocs['imlicencevoc'] = (('lic1', u'CCbySA'), ('lic2', u'Copyright'), )
    # imVocs['imlicencevoc'] = []
    return imVocs

class imMetadatas:
    listVocabularies = []
    listVocabularies.append('imlocationvoc')
    listVocabularies.append('imtagvoc')
    listVocabularies.append('imscitagvoc')
    listVocabularies.append('imteamvoc')
    listVocabularies.append('improjectvoc')
    listVocabularies.append('improjectvoc')
    listVocabularies.append('imlicencevoc')
    
    vocabMetadata = {}
    vocabMetadata['general'] = 'imtagvoc'
    vocabMetadata['science'] = 'imscitagvoc'
    vocabMetadata['where'] = 'imlocationvoc'
    vocabMetadata['laboratory'] = 'imteamvoc'
    vocabMetadata['reseachproject'] = 'improjectvoc'
    vocabMetadata['licencetype'] = 'imlicencevoc'

def initImVocs(context):
    """ 
    Create Vocabularies defined in defineImVocs
    This method is called at iuem.photorepository install time
    """
    imVocs=defineImVocs(context) 
    portal=context.getSite()
    try:
        ATVocTools = getToolByName(getToolByName(portal,'portal_url').getPortalObject(), ATVOCABULARYTOOL)
    except:
        return
    # ATVocTools = getToolByName(context , 'portal_vocabularies')
    for imVocKey in imVocs.keys():
        if not hasattr(ATVocTools, imVocKey):
            ATVocTools.invokeFactory('SimpleVocabulary', imVocKey)
            print("Creating imVocubaluries",imVocKey)
            vocab = ATVocTools[imVocKey]
            for (imkey, value) in imVocs[imVocKey]:
                if not hasattr(vocab, imkey):
                    vocab.invokeFactory('SimpleVocabularyTerm', imkey)
                    vocab[imkey].setTitle(value)

class IUpdateVocabs(Interface):
    def __call__(context):
        """Interface to vocalularies updater
        """

class UpdateVocabs(object):
    implements(IUpdateVocabs)
    
    def __call__(context):
        import pdb;pdb.set_trace()
        """
        vocabs = getToolByName(context , 'portal_vocabularies')
        FORM = context.request.form
        for k in FORM.keys():
            # print k + ' ' + FORM[k]
            if k == 'where':
                val = FORM[k]
                vocab = vocabs['imlocationvoc']
                if not hasattr(vocab, val) and val:
                    vocab.invokeFactory('SimpleVocabularyTerm', val)
                    vocab[val].setTitle(val)
         """
    
class UpdateVocs(BrowserView):
        
    def __call__(context):
        # import pdb;pdb.set_trace()

        vocabs = getToolByName(context , 'portal_vocabularies')
        FORM = context.request.form
        for k in FORM.keys():
            # print k + ' ' + FORM[k]
            if k == 'where':
                val = FORM[k]
                vocab = vocabs['imlocationvoc']
                if not hasattr(vocab, val) and val:
                    vocab.invokeFactory('SimpleVocabularyTerm', val)
                    vocab[val].setTitle(val)
        # import pdb;pdb.set_trace()
            
        
        
