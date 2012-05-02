from z3c.form import validator
from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator


class isLatitude:
    """Verify valid latitude input
    """
    implements(IValidator)
    
    def __init__(self, name , title='isLatitude', description='isLatitude Descr'):
        self.name = name
        self.title = title
        self.description = description
        
    def __call__(self, value, *args, **kwargs):
        # print "in method 'validate' of isLatitude class"
        return None
    
class isLongitude:
    """Verify valid longitude input
    """
    implements(IValidator)
    
    def __init__(self, name , title='isLongitude', description='isLongitude Descr'):
        self.name = name
        self.title = title
        self.description = description

    
    def __call__(self, value, *args, **kwargs):
        # print "in method 'validate' of isLongitude class"
        return None