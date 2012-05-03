from zope import interface
from zope import schema
from zope.component import adapts
from Products.ATContentTypes.interface import IATFolder

from plone.autoform.form import AutoExtensibleForm

from z3c.form import form , field , button , error
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError

from plone.z3cform import layout
from Products.statusmessages.interfaces import IStatusMessage

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

class ManageMetadataForm(AutoExtensibleForm , form.Form):
    """The form"""
    adapts(IATFolder)
    fields = field.Fields(IManageMetadataForm)

    # desactive ignoreContext et on surcharge la methode getContent
    # afin de pre-remplir le formulaire avec les valeurs existantes
    ignoreContext = True
    
    label = u"distribute metadata values among objects"
    description = u"Decide where to spread metadatas"
    
    # context = getContent()
    # context = update()
    
    # import pdb;pdb.set_trace()

    def update(self):
        context = self.context
        return context
    
    def getContent(self):
        context = self.context
        # import pdb;pdb.set_trace()
        return context

ManageMetadataFormView = layout.wrap_form(ManageMetadataForm)    

