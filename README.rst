Introduction
============
Plone 4 products to manage Photos repository

I'm new in plone development and this product is my first product.
So advises, corrections and suggestions are really welcome !

This product has to satisfy a need in my institute (IUEM, Institut Universitaire
Européen de la Mer, www-iuem.univ-brest.fr) and was initiated by the communication
service.

Special Thanks to :
===================
Bertrand Gobert : communication service in IUEM

Jean-Michel François (aka toutpt) for his courses

Tristan Le Toullec (new plone integrator and developer in IUEM) 

Features :
========== 

The two main ideas of this product are :

1- extend metadatas for a finer grain research and selection

2- spread folders metadatas to contained objects

This product aim to make your entire plone site dedicated for photos/images
repository. Large use of archetypes.schemaextender is done to extend metadatas
of folder and images. So _ALL_ folders and images are extended.

When you add a new folder or image, you can use metadatas already included in
the vocabularies (like a thesaurus) or add new values which are added to the
vocabularies when you save your new object.

collective.quickupload is a dependency of this product because we want that the
photos upload easy for users. When this process is used, it's a good idea to spread
the container metadatas to the inserted photos.

Because eea.facetednavigation seems to be very good tool to browse the database,
a special search form wasn't developed.   
 
