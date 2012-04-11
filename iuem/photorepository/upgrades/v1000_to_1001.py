from Products.CMFCore.utils import getToolByName

def upgrade_1000_to_1001(context):
    setup = getToolByName(context, 'portal_setup')
#    setup.runImportStepFromProfile('profile-iuem.photorepository:default',
#                                   'jsregistry', run_dependencies=False,
#                                   purge_old=False)
