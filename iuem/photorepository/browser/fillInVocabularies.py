# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from iuem.photorepository.manageVocabulary import imMetadatas
from iuem.photorepository.extender import ImageImageRepositoryExtender
from iuem.photorepository.extender import FolderImageRepositoryExtender
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer

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
        vocDict = {}
        vocDict['general_voc'] = ['Ifremer','Navire','Mission','Pluridisciplinarité','Géologie','Biologie','Milieux Extrêmes','Environnement côtier']
        vocDict['laboratory_voc'] = ['LPO','LEMAR','GEOMER','UMS3113','LM2E']
        vocDict['localization_voc'] = ['Rade de Brest','Océan Pacifique','Plouzané',"Mer d'Iroise","Océan Atlantique","Mer des Caraïbes"]
        vocDict['science_voc'] = ['Palourde','Coquille Saint Jacques','Dorsale Atlantique','Lamellibranches','Dulcicoles','Polyplacophores','Gastéropodes','Céphalopodes']
        vocDict['researchproj_voc'] = ['EPURE','ECOTAB','LabexMer','PERISCOPE']
        vocDict['licencetype_voc'] = ['GPL','Usage Totalement Libre','Creative Commons','LGPL','BSD']
        
        normalizer = getUtility(INormalizer)
        vocabs['general_voc'].addTerm(key='lacle' , value = u'La clé' , termtype='SimpleVocabularyTerm',silentignore=True)
        for keys in vocDict:
            # print keys
            for k in vocDict[keys]:
                normalizedk = normalizer.normalize(unicode(k,'utf-8'), locale = 'fr')
                # print '    ' + str(k) + ':' + normalizedk
                vocabs[keys].addTerm(key=normalizedk , value = k , termtype='SimpleVocabularyTerm',silentignore=True)
        return vocDict
        # import pdb;pdb.set_trace()