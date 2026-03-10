# -*- coding: utf-8 -*-
from eteaching.plone.nostrmetadatasync.testing import FUNCTIONAL_TESTING
from eteaching.plone.nostrmetadatasync.testing import INTEGRATION_TESTING
from eteaching.plone.nostrmetadatasync.controlpanels.controlpanel import INostrMetadataSyncMangementControlpanel
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_nostr_metadata_sync_mangement_controlpanel_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='nostr-metadata-sync-mangement-controlpanel'
        )
        self.assertTrue(INostrMetadataSyncMangementControlpanel.providedBy(view))

    def test_nostr_metadata_sync_mangement_controlpanel_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='nostr-metadata-sync-mangement-controlpanel'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = INostrMetadataSyncMangementControlpanel.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
