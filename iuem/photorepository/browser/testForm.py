# from zope import interface
from zope import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form.form import Form
from plone.z3cform import layout
from plone.directives import form
import datetime

class ITestForm(form.Schema):
    """ItestForm"""
    vehicle = schema.Choice(title=u"Choice your vehicle",
                            description=u"for our next trip",
                            values=['Ferry boat','Car','Truck','motorcycle'])
    destination = schema.Choice(title=u"Where" ,
                                description=u"short or long trip",
                                values=['Brest','Brazil','Italia','Paris'])
    commentaire = schema.Text(title=u"Commentaire")
    start = schema.Datetime(title=u"Start date",
                            required=False
    )

@form.default_value(field=ITestForm['start'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)

@form.default_value(field=ITestForm['commentaire'])
def vehicleDefaulValue(data):
    return u"Car"


class TestForm(AutoExtensibleForm, Form):
    schema = ITestForm
    ignoreContext = False
    
    method = "post"
    
    def getContent(self):
        context = self.context
        data = {}
        data['commentaire'] = unicode(context.Description() , 'utf-8')
        return data
            
    @button.buttonAndHandler(u"Ok, have a good trip")
    def goodTrip(self, action):
        data , errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # changes = self.applyChanges(data)
        request = self.request
        print request.form
        print '-------'
        print data
        # nextUrl = '%s/@@test_view' % (self.context.absolute_url())
        # import pdb;pdb.set_trace()
        # request.response.redirect(nextUrl)
    
    def action(self):
        return self.context.absolute_url() + '/@@test_view'

class TestFormView(layout.FormWrapper):
    label = u"Choice your trip here"
    form = TestForm
    