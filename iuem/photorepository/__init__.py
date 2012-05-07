

from Products.validation import validation
from validators import isLatitude , isLongitude

from zope.i18nmessageid import MessageFactory
iuemMessageFactory = MessageFactory('iuem.photorepository')


validation.register(isLatitude('isLatitude'))
validation.register(isLongitude('isLongitude'))
