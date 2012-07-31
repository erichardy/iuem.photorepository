Introduction
============
Plone 4 products to manage Photos repository

I'm new in plone development and this is my first product.
So advise, corrections and suggestions are really welcome !

This product is meant to satisfy a need at the institute where I work (IUEM,
Institut Universitaire Européen de la Mer, www-iuem.univ-brest.fr) and was
initiated by the communication service.

Special Thanks to :
===================
Bertrand Gobert : communication service in IUEM

Jean-Michel François (aka toutpt) for his courses

Tristan Le Toullec (new plone integrator and developer in IUEM) 

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

collective.quickupload is a dependency of this product because we want that the
photos upload easy for users. When this process is used, it's a good idea to spread
the container metadatas to the inserted photos.

Because eea.facetednavigation seems to be very good tool to browse the database,
I haven't developed a special search form.   
 
