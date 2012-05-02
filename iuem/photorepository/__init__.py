

from Products.validation import validation
from validators import isLatitude , isLongitude

validation.register(isLatitude('isLatitude'))
validation.register(isLongitude('isLongitude'))
