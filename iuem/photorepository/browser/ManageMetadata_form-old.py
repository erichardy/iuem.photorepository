from zope import interface
from zope import schema
from zope.component import adapts
from Products.ATContentTypes.interface import IATFolder
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from iuem.photorepository import iuemMessageFactory as _

from plone.autoform.form import AutoExtensibleForm

from z3c.form import form , field , button , error
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError

from plone.z3cform import layout
from Products.statusmessages.interfaces import IStatusMessage

def possibleWhere(self,context):
    adapts(IContextSourceBinder)
    w = []
    for ww in context.where:
        w.append(SimpleVocabulary.createTerm(ww,ww,ww))
    print context.where
    return SimpleVocabulary(w)


class IManageMetadataForm(interface.Interface):
    """metadata form"""
    """
    ptype = schema.Choice(title=u"Type", description=u"File type",values=['test'])
    autor = schema.ASCIILine(title=u"Auteur",
                             description=u"a person")
    """
    whereToSpread = schema.Choice(title=u"Where to spread",
                                  description=u"Description where to spread",
                                  values=['only Images','everywhere'])
    where = schema.Set(title=u"Localisation",
                                  description=_(u"Localisations"),
                                  value_type=schema.Choice(source=possibleWhere)
                                  )
    

class ManageMetadataForm(AutoExtensibleForm, form.Form):
    """The form"""
    adapts(IATFolder)
    fields = field.Fields(IManageMetadataForm)
    ignoreContext = True
    
    label = u"distribute metadata values among objects"
    description = u"Decide where to spread metadatas"
    
    # import pdb;pdb.set_trace()

    def getContent(self):
        context = self.context
        # import pdb;pdb.set_trace()
        x = 'retour de getContent()'
        data = {}
        data['where'] = ['ici','et la']
        
        return data
    
    @button.buttonAndHandler(u'Ok')
    def handleOk(self, action):
        data, errors = self.extractData()
        
        if errors:
            self.status = self.formErrorsMessage
            return
    
        
        
ManageMetadataFormView = layout.wrap_form(ManageMetadataForm)    

