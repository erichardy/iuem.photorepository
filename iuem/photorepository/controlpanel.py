from plone.app.registry.browser import controlpanel
from iuem.photorepository.interfaces import IPhotorepositorySettings

from iuem.photorepository import iuemRepositoryMessageFactory as _

class PhotorepositorySettingsForm(controlpanel.RegistryEditForm):
    schema = IPhotorepositorySettings
    label = _(u"Photorepository Settings")
    description = _(u"PhotorepositorySettingsDescription")
    
    def updateFields(self):
        super(PhotorepositorySettingsForm , self).updateFields()

    def updateWidgets(self):
        super(PhotorepositorySettingsForm , self).updateWidgets()

class PhotorepositorySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PhotorepositorySettingsForm

