import logging

from plone import api
from plone.base.interfaces.installable import INonInstallable
from zope.interface import implementer

logger = logging.getLogger(__name__)


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "eteaching.plone.nostrmetadatasync:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return [
            "eteaching.plone.nostrmetadatasync.upgrades",
        ]


def post_install(context):
    """Post install script"""


def uninstall(context):
    """Uninstall script"""
    unregister_controlpanel()


def unregister_controlpanel():
    t = "Unregister controlpanel NostrMetadataSyncMangement."
    cp = api.portal.get_tool("portal_controlpanel")
    cp.unregisterConfiglet("nostrmetadatasync-management")
    logger.info(f"{t} [OK]")
