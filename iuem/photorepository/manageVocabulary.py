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
    imVocs['localization_voc'] = (('brest',u'Brest'),('plouzane',u'Plouzané'), )
    # imVocs['localization_voc'] = []
    imVocs['general_voc'] = (('mer', u'Mer'), ('navire', u'Navire'), )
    # imVocs['general_voc'] = []
    imVocs['science_voc'] = (('adcp', u'ADCP'), ('mouillage', u'Mouillage'), )
    # imVocs['science_voc'] = []
    imVocs['laboratory_voc'] = (('lemar', u'LEMAR'), ('lm2e', u'LMEE'),('lpo', u'LPO'))
    # imVocs['laboratory_voc'] = []
    imVocs['researchproj_voc'] = (('aspex', u'Aspex'), ('epure', u'EPURE'), )
    # imVocs['researchproj_voc'] = []
    imVocs['licencetype_voc'] = ()
    imVocs['photographer_voc'] = ()
    # imVocs['licencetype_voc'] = []
    return imVocs

class imMetadatas:
    listVocabularies = []
    listVocabularies.append('localization_voc')
    listVocabularies.append('general_voc')
    listVocabularies.append('science_voc')
    listVocabularies.append('laboratory_voc')
    listVocabularies.append('researchproj_voc')
    listVocabularies.append('licencetype_voc')
    listVocabularies.append('photographer_voc')
    
    vocabMetadata = {}
    vocabMetadata['general'] = 'general_voc'
    vocabMetadata['science'] = 'science_voc'
    vocabMetadata['where'] = 'localization_voc'
    vocabMetadata['laboratory'] = 'laboratory_voc'
    vocabMetadata['reseachproject'] = 'researchproj_voc'
    vocabMetadata['licencetype'] = 'licencetype_voc'
    vocabMetadata['photographer'] = 'photographer_voc'
    
    commonMetadatas = []
    commonMetadatas.append('description')
    commonMetadatas.append('general')
    commonMetadatas.append('science')
    commonMetadatas.append('where')
    commonMetadatas.append('laboratory')
    commonMetadatas.append('reseachproject')
    commonMetadatas.append('licencetype')
    commonMetadatas.append('recording_date_time')
    commonMetadatas.append('photographer')
    commonMetadatas.append('watermark')

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
            print("Creating Empty imVocubaluries",imVocKey)
            """
            vocab = ATVocTools[imVocKey]
            for (imkey, value) in imVocs[imVocKey]:
                if not hasattr(vocab, imkey):
                    vocab.invokeFactory('SimpleVocabularyTerm', imkey)
                    vocab[imkey].setTitle(value)
            """
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
                vocab = vocabs['localization_voc']
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
                vocab = vocabs['localization_voc']
                if not hasattr(vocab, val) and val:
                    vocab.invokeFactory('SimpleVocabularyTerm', val)
                    vocab[val].setTitle(val)
        # import pdb;pdb.set_trace()
            
        
        
