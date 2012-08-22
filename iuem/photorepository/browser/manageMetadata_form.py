# -*- coding: utf-8 -*-
import logging
from Products.Five import BrowserView
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('iuem.photorepository')

class ManageMetadataFormView(BrowserView):    
    adapts(IATFolder)

    def __call__(self):
        # print self.request.form
        return self.index()

    def kwValue(self , kw):
        context = self.context
        if context[kw] == None:
            return False
        if kw == 'recording_date_time':
            return context[kw]
        if len(context[kw]) > 0:
            return context[kw]
        else:
            return False

    def value_of (self , value , vocabulary):
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        try:
            vocab = myVocabsTool[vocabulary]
            return vocab.getVocabularyDict()[value]
        except:
            return '' 
                
        
        
        
        