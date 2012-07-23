# -*- coding: utf-8 -*-
from Products.Five import BrowserView
# from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from zope.component import adapts
from Products.CMFCore.utils import getToolByName

class ManageMetadataFormView(BrowserView):    
    adapts(IATFolder)

    def __call__(self):
        # print self.request.form
        return self.index()
    
    def description(self):
        try:
            desc = self.context.Description()
            return desc
        except:
            return False
    
    def general(self):
        try:
            return self.context.general
        except:
            return False        
    
    def science(self):
        try:
            return self.context.science
        except:
            return False
    
    def where(self):
        try:
            return self.context.where
        except:
            return False
    
    def laboratory(self):
        try:
            return self.context.laboratory
        except:
            return False
    
    def reseachproject(self):
        try:
            return self.context.reseachproject
        except:
            return False
    
    def licencetype(self):
        try:
            return self.context.licencetype
        except:
            return False
    
    def recording_date_time(self):
        try:
            return self.context.recording_date_time
        except:
            return False
    
    def photographer(self):
        try:
            return self.context.photographer
        except:
            return False
    
    def value_of (self , value , vocabulary):
        myVocabsTool = getToolByName(self.context , 'portal_vocabularies')
        try:
            vocab = myVocabsTool[vocabulary]
            return vocab.getVocabularyDict()[value]
        except:
            return '' 
                
        
        
        
        