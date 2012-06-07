To manage translations :

cd iuem.photorepository/iuem/photorepository

in __init__.py :
from zope.i18nmessageid import MessageFactory
iuemRepositoryMessageFactory = MessageFactory('iuem.photorepository')

to make .pot file :
i18ndude rebuild-pot --create iuem.photorepository --pot locales/iuem.photorepository.pot --exclude="ManageMetadata_form-bug.py ManageMetadata_form-old.py" .

to sync .po file :
i18ndude sync --pot locales/iuem.photorepository.pot locales/fr/LC_MESSAGES/iuem.photorepository.po
-> enter french translations in the file iuem.photorepository.po

in ZPT templates :
<tag i18n:translate="label_to_translate">Label to translate</tag>

in .py :
from iuem.photorepository import iuemRepositoryMessageFactory as _
...
	message = _(u'label_to_translate')



See : http://plone.org/documentation/manual/developer-manual/internationalization-i18n-and-localization-l10n

