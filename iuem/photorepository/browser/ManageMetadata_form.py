from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button , field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import adapts
from Products.ATContentTypes.interface import IATFolder
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from iuem.photorepository import iuemMessageFactory as _
from Products.AddRemoveWidget import AddRemoveWidget
from plone.z3cform import layout
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer

class metadataSource(object):
    grok.implements(IContextSourceBinder)
    def __init__(self,k):
        self.k = k
    def __call__(self , context):
        w = []
        for ww in context[self.k]:
            normalizer = getUtility(INormalizer)
            nww = normalizer.normalize(unicode(ww , 'utf-8'), locale = 'fr')
            uww = unicode(ww , 'utf-8')
            w.append(SimpleVocabulary.createTerm(nww,nww,uww))   
        return SimpleVocabulary(w)
class stdMetadataSource(object):
    grok.implements(IContextSourceBinder)
    def __init__(self,k):
        self.k = k
    def __call__(self , context):
        return SimpleVocabulary

class IManageMetadataForm(form.schema.Schema):
    """metadata form"""
    """
    ptype = schema.Choice(title=u"Type", description=u"File type",values=['test'])
    autor = schema.ASCIILine(title=u"Auteur",
                             description=u"a person")
    """
    whereToSpread  = schema.Choice(title=u"Where to spread",
                     required=False,
                     description=u"Description where to spread",
                     values=['only Images','everywhere']
                     )
    addOrReplace   = schema.Choice(title=_(u"addOrPreplace"),
                     required=False,
                     description=_(u"addOrReplaceDesc"),
                     values=['add','replace'],
                     default='add'
                     )
    xdescription   = schema.Text(title=u"Description",
                     required=False,
                     description=_(u"Description")
                     )
    where          = schema.Set(title=u"Localisation",
                     required=False,
                     description=_(u"Localisations"),
                     value_type=schema.Choice(source=metadataSource('where'))
                     )
    laboratory     = schema.Set(title=u"Laboratory",
                     required=False,
                     description=_(u"Laboratories"),
                     value_type=schema.Choice(source=metadataSource('laboratory'))
                     )
    reseachproject = schema.Set(title=u"reseachproject",
                     required=False,
                     description=_(u"reseachproject"),
                     value_type=schema.Choice(source=metadataSource('reseachproject'))
                     )

class ManageMetadataForm(form.form.SchemaForm):
    """The form"""
    grok.name('manage_metadata')
    grok.require('zope2.View')
    grok.context(IATFolder)
    
    schema = IManageMetadataForm
    ignoreContext = True
    
    label = u"distribute metadata values among objects"
    description = u"Decide where to spread metadatas"
    fields = field.Fields(IManageMetadataForm)
    fields['where'].widgetFactory = CheckBoxFieldWidget
    fields['laboratory'].widgetFactory = CheckBoxFieldWidget
    fields['reseachproject'].widgetFactory = CheckBoxFieldWidget
    # print dir(fields['xdescription'])
    # fields['xdescription'].ignoreContext = False

    def getContent(self):
        context = self.context
        data = {}
        data['xdescription'] = context.Description()
        data['where'] = context.where
        data['laboratory'] = context.laboratory
        data['reseachproject'] = context.reseachproject
        print context.Description()
        return data
        
    @button.buttonAndHandler(u'Ok',accessKey=u"o")
    def handleOk(self, action):
        data, errors = self.extractData()
        print data
        # print '============================'
        # print errors
        if errors:
            self.status = self.formErrorsMessage
            return
        request = self.request
        # nextUrl = '%s/@@metadata_view_pt'%self.context.absolute_url()
        nextUrl = self.context.absolute_url()
        request.response.redirect(nextUrl)


@form.default_value(field=IManageMetadataForm['where'])
def defWhere(data):
    return ['plouzane']
        
ManageMetadataFormView = layout.wrap_form(ManageMetadataForm)    

