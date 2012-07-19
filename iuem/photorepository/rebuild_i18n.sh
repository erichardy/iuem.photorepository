#!/bin/sh
PRODUCTNAME='iuem.photorepository'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} --exclude="./browser/ManageMetadata_form-bug.py" .

# Synchronise the resulting .pot with the .po files
# i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po

# A faire :
# i18ndude find-untranslated browser/*.pt | less
