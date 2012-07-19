Introduction
============
Plone 4 products to manage Photo repository

External helpful documentations
-------------------------------
Event handlers :
- http://plone.org/documentation/kb/five-zope3-walkthrough/events

- http://plone.org/documentation/manual/developer-manual/archetypes/other-useful-archetypes-features/how-to-use-events-to-hook-the-archetypes-creation-process

- http://plone.org/documentation/manual/developer-manual/archetypes/appendix-practicals/b-org-creating-content-types-the-plone-2.5-way/sending-and-handling-events

Manipulating images :
- http://collective-docs.readthedocs.org/en/latest/images/content.html

Un bug qui persiste : apres avoir procede a la propagation de metadonnees, si on ajoute un dossier ou
une image, certains champs sont pre-remplis avec des valeurs. Ca semble aleatoire autant en ce qui
concerne le type d'objet ajoute que les champs eux-memes....????
C'est comme si les champs de metadonnees etaient pre-remplis lors de l'appel au formulaire d'ajout
Ce n'est pas dependant du navigateur.
Si on re-demarre le serveur, les champs sont bien re-initialises ˆ 'rien'
En tout cas, c'est particulierement difficile a reproduire....

patch de eea.facetednavigation-4.8-py2.6.egg/eea/facetednavigation/views/preview-item.pt
<a ...
   ...
   urlview string:${url}/view;
   ...
   tal:attributes="href urlview; title description;target string:_blank">


   
