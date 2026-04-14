"""Init and utils."""

import logging

from zope.i18nmessageid import MessageFactory

__version__ = "1.0.0b2"

PACKAGE_NAME = "eteaching.plone.nostrmetadatasync"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
