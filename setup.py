from setuptools import setup, find_packages
import os

version = '1.0b1'

setup(name='iuem.photorepository',
      version=version,
      description="Addon for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        ],
      keywords='image repository',
      author='Eric Hardy',
      author_email='Eric.Hardy@univ-brest.fr',
      url='https://github.com/erichardy/iuem.photorepository',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iuem'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          'plone.directives.form',
          'collective.quickupload',
          'pillow',
          'plone.app.theming',
          'plone.api',
          'archetypes.schemaextender',
          'plone.app.registry',
          'Products.ATVocabularyManager==1.6.2',
          'eea.facetednavigation==5.0',
          'Products.AddRemoveWidget',
          'collective.js.jqueryui',
          # -*- Extra requirements: -*-
      ],
      extras_require = dict(
          tests=['plone.app.testing'],
      ),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
