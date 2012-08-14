from zope.interface import Interface
from zope.interface import implements
from zope.schema import Text

from z3c.form import field , form
from zope.component import adapts
from Products.ATContentTypes.interface import IATImage

# from plone.directives import form


class IqueryImage(Interface):
    """
    """
    text = Text(
                title = u"Preesentation Text",
                description = u"preesentation Description",
                required = True
                )
    
class queryImage(form.Form):
    adapts(IATImage)
    implements(IqueryImage)
    fields = field.Fields(IqueryImage)
    label = u"le label de queyImage"
    ingnorecontext = True