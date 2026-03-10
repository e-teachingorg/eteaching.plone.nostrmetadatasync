# -*- coding: utf-8 -*-

from eteaching.plone.nostrmetadatasync import _
from plone import api
from plone.app.registry.browser import controlpanel
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from eteaching.plone.nostrmetadatasync import base
from eteaching.plone.nostrmetadatasync.interfaces import INostrMetadataSyncSettings

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INostrMetadataSyncMangementControlpanel(Interface):
    """ Marker Interface for INostrMetadataSyncMangementControlpanel"""


@implementer(INostrMetadataSyncMangementControlpanel)
class NostrMetadataSyncMangementControlpanel(BrowserView):

    def __call__(self):

        create = self.request.get("create")
        delete = self.request.get("delete")

        if create:
            try:
                result = base.create_all_events()
            except Exception as e:
                result = e
            api.portal.show_message(message=result, request=self.request)

        elif delete:
            try:
                result = base.delete_all_events()
            except Exception as e:
                result = e
            api.portal.show_message(message=result, request=self.request)

        return self.index()


class NostrMetadataSyncSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INostrMetadataSyncSettings
    schema_prefix = "nostrmetadatasync-settings"
    label = _("NostrMetadataSync settings")
    description = ""

    def updateFields(self):
        super(NostrMetadataSyncSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(NostrMetadataSyncSettingsEditForm, self).updateWidgets()


class NostrMetadataSyncSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NostrMetadataSyncSettingsEditForm


class Setup(BrowserView):

    def reimportProfile(self):
        """ Reimport eteaching.plone.openbadges profile """
        portal_setup = self.context.portal_setup
        portal_setup.manage_importAllSteps(
            context_id="profile-eteaching.plone.nostrmetadatasync:default"
        )
        self.context.plone_utils.addPortalMessage(
            "profile-eteaching.plone.nostrmetadatasync profile reimported"
        )
        self.request.response.redirect(self.context.absolute_url())
