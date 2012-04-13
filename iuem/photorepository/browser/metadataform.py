from zope import interface
from zope import schema

from plone.autoform.form import AutoExtensibleForm

from z3c.form import form , button , error
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError

from plone.z3cform import layout
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from iuem.photorepository.metadatamanager import IMetadaManager
from Products.statusmessages.interfaces import IStatusMessage

class IMetadataForm(interface.Interface):
    """metadata form"""
    ptype = schema.ASCIILine(title=u"Type",
                             description=u"JPEG, GIF, TIFF, RAW,....")
    autor = schema.ASCIILine(title=u"Auteur",
                             description=u"a person")


class MetadataForm(AutoExtensibleForm , form.Form):
    """The form"""
    schema = IMetadataForm
    # desactive ignoreContext et on surcharge la methode getContent
    # afin de pre-remplie le formulaire avec les valeurs existantes
    ignoreContext = False
    
    def getContent(self):
        mm = IMetadaManager(self.context)
        try:
            content = mm.read()
        except:
            content={}
        return content
    
    @button.buttonAndHandler(u"Save")
    def save(self,action):
        data , errors = self.extractData()
        if errors:
            return
        ptype = data.get('ptype')
        if ptype not in ['JPEG', 'GIF' , 'RAW']:
            raise WidgetActionExecutionError('ptype', interface.Invalid(u"RTFM...!"))

        mm = IMetadaManager(self.context)
        try:
            mm.write(data)
        except ValueError:
            IStatusMessage(self.context).add('Error in data')
        #        import pdb ; pdb.set_trace()
        request = self.request
        nextUrl = '%s/@@metadata_view_pt'%self.context.absolute_url()
        request.response.redirect(nextUrl)
    

class MetadataFormView(layout.FormWrapper):
    label = u"The form wrapper"
    form = MetadataForm
    