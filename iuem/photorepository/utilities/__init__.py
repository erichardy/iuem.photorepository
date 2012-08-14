##################################################################################
#    Copyright (c) 2004-2009 Utah State University, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
##################################################################################

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]

import unicodedata
from os import close
import tempfile
from os.path import split, splitext
from urllib import unquote

from zope.component import queryUtility
from zope.interface import implements
try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from OFS.SimpleItem import SimpleItem

from Products.ATContentTypes import interfaces
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName

from plone.i18n.normalizer.interfaces import IURLNormalizer

from zipfile import ZipFile, ZIP_DEFLATED

from tempfile import TemporaryFile

#
from zope.event import notify
from Products.Archetypes.event import ObjectInitializedEvent
#


def _patchedcreateObject(self, filepath, fdata, parent):
    """ """
    props = getToolByName(parent, 'portal_properties')
    image_type = props.zipfile_properties.image_type
    file_type = props.zipfile_properties.file_type
    doc_type = props.zipfile_properties.doc_type
    folder_type = props.zipfile_properties.folder_type

    mt = parent.mimetypes_registry

    ext = filepath.split('.')[-1]
    ext = ext.lower()
    ftype = mt.lookupExtension(ext)
    if ftype:
        mimetype = ftype.normalized()
        newObjType = self._getFileObjectType(ftype.major(), mimetype)
    else:
        newObjType = self._getFileObjectType(
                                    'application',
                                    'application/octet-stream'
                                    )
        mimetype = 'application/octet-stream'
    nm = filepath.split('/')

    if nm[-1]:
        filename = nm[-1]
    else:
        filename = nm[0]

    if filename not in parent.objectIds():
        parent.invokeFactory(type_name=newObjType, id=filename)
        obj = getattr(parent, filename)
        obj.setTitle(splitext(filename)[0])
    else:
        obj = getattr(parent, filename)

    if newObjType == image_type:
        obj.setImage(fdata)
    elif newObjType == doc_type:
        obj.setText(fdata)
    elif newObjType == file_type:
        obj.setFile(fdata)

    factory = getToolByName(parent, 'portal_factory')
    catalog = getToolByName(parent, 'portal_catalog')
    obj = factory.doCreate(obj, filename)
    obj.setFormat(mimetype)
    notify(ObjectInitializedEvent(obj))
    catalog.reindexObject(obj, catalog.indexes())
    return obj

