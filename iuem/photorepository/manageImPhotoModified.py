

def imIObjectModifiedEvent(obj):
    print str(obj.object.id) + ' Modified'

def imIObjectRemovedEvent(obj):
    print str(obj.object.id) + ' Removed'

def imIObjectCopiedEvent(obj):
    print str(obj.object.id) + ' Copied'

def imIObjectMovedEvent(obj):
    print str(obj.object.id) + ' Moved'

