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

Tristan LE TOULLEC (new plone integrator and developer in IUEM) 

Features :
========== 

The two main ideas of this product are :

1- to add metadata for a finer grain research and selection

2- to attribute folder metadata to contained

This product aims to dedicate your entire Plone site to a photos/images
repository. Archetypes.schemaextender is largely used to extend metadata of
folders and images. So _ALL_ folders and images are extended.

When you add a new folder or image, you can use metadatas already included in
the vocabularies (like a thesaurus) or add new values which are added to the
vocabularies when you save your new object.

When an image is uploaded, the original image is copied to a new field and
the Image field is modified : it is reduced and to diagonal lines
are drawn. Only a user with permission 'iuem.photorepository: View Full Image',
owner and manager by default, can access the original image.

Because eea.facetednavigation seems to be very good tool to browse the database,
I haven't developed a special search form.   
 
We use collective.quickupload to upload groups of photos

Installation :
==============

Just add iuem.photorepository to egg section of your buildout.cfg


TODO :
======

- really manage watermarks
- latitude and longitude fields : how to set values....?
- config view to manage some parameters : image transformation, watermarks,
  permissions, etc...

TEMP test
=========
test with branches
modif for more test...