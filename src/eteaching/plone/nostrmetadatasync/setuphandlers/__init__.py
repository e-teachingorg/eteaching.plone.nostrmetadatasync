from plone.base.interfaces.installable import INonInstallable
from zope.interface import implementer


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
