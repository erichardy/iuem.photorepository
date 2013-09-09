Introduction
============
Plone 4 products to manage Photos repository

I'm new in plone development and this is my first product.
So advise, corrections and suggestions are really welcome !

This product is meant to satisfy a need at the institute where I work (IUEM,
Institut Universitaire Europeen de la Mer, www-iuem.univ-brest.fr) and was
initiated by the communication service.

Special Thanks to :
===================
Bertrand GOBERT : communication service in IUEM

Jean-Michel FRANCOIS (aka toutpt) for his courses

Tristan LE TOULLEC (plone integrator and developer in IUEM)

Valentin Cadot (student who worked on this for 3 months)

Features :
========== 

The two main ideas of this product are :

1- to add metadata for a finer grain research and selection

2- to attribute/spread folder metadata to contained images and folders

This product aims to dedicate your entire Plone site to a photos/images
repository. Archetypes.schemaextender is largely used to extend metadata of
folders and images. So _ALL_ folders and images are extended.

When you add a new folder or image, you can use metadata already included in
the vocabularies (like a thesaurus) or add new values which are added to the
vocabularies when you save your new object.

When an image is uploaded, the original image is copied to a new field and
the Image field is modified : it is reduced and a watermark is applied.
Only a user with permission 'iuem.photorepository: View Full Image',
owner and manager by default, can access the original image.

Because eea.facetednavigation is a very good tool to browse the database,
I didn't develop a special search form.   

collective.quickupload is recommended to upload groups of photos, but the module
collective.zipfiletransport is also used.

Installation :
==============

Just add iuem.photorepository to egg list in your buildout.cfg


TODO :
======

- latitude and longitude fields : how to set values....?
- config view to manage some parameters : image transformation, permissions, etc...
- full documentation for users and repository manager

