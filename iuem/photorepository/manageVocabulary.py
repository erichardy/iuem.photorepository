# -*- coding: utf-8 -*-
"""
Various tools to manage iuem.photorepository vocabularies
"""
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager import NamedVocabulary
from zope.app.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary


def defineImVocs(self):
    imVocs = {}
    imVocs['imtypevoc'] = (('type1', u'jpeg'), ('type2', u'tiff'), ('type3', u'png'),('type4', u'gif'),('type5', u'psd'), )
    imVocs['imlocationvoc'] = (('loc1,',u'Brest'),('loc2,',u'Plouzané'),('loc3,',u'Golf de Gascogne'), )
    imVocs['imtagvoc'] = (('tag1', u'Mer'), ('tag2', u'Navire'), )
    imVocs['imscitagvoc'] = (('scitag1', u'ADCP'), ('scitag2', u'Mouillage'), )
    imVocs['imteamvoc'] = (('team1', u'LEMAR'), ('team2', u'Domaine Océanique'), ('team3', u'LMEE'),('team4', u'LPO'))
    imVocs['improjectvoc'] = (('camp1', u'Aspex'), ('camp2', u'Fromvar'), )
    imVocs['imlicencevoc'] = (('lic1', u'CCbySA'), ('lic2', u'Copyright'), )
    return imVocs

def initImVocs(context):
    """ 
    Create Vocabularies defined in defineImVocs
    This method is called at iuem.photorepository install time
    """
    imVocs=defineImVocs(context) 
    portal=context.getSite()
    ATVocTools = getToolByName(getToolByName(portal,'portal_url').getPortalObject(), ATVOCABULARYTOOL)
    
    for imVocKey in imVocs.keys():
        if not hasattr(ATVocTools, imVocKey):
            ATVocTools.invokeFactory('SimpleVocabulary', imVocKey)
            print("Creating imVocubaluries",imVocKey)
            vocab = ATVocTools[imVocKey]
            for (imkey, value) in imVocs[imVocKey]:
                if not hasattr(vocab, imkey):
                    vocab.invokeFactory('SimpleVocabularyTerm', imkey)
                    vocab[imkey].setTitle(value)