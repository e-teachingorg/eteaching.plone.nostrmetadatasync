from DateTime import DateTime
from plone import api
from Products.ZCatalog.interfaces import ICatalogBrain
from pynostr.event import Event
from zope.globalrequest import getRequest
from zope.i18n import translate

from eteaching.plone.nostrmetadatasync import _, client
from eteaching.plone.nostrmetadatasync.interfaces import (
    INostrAmbEvent,
    INostrTimeBasedCalendarEvent,
)
from eteaching.plone.nostrmetadatasync.utils import get_brains


def create_events(objs, INostrEvent):
    """Creates Nostr events using a list of objects and a passed adapter and
    publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager()

    for i in objs:

        obj = i.getObject() if ICatalogBrain.providedBy(i) else i

        c = INostrEvent(obj)
        event = Event(kind=c.kind(), content=c.content(), tags=c.tags())
        client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager)

    return counter


def delete_events(objs, INostrEvent):
    """Creates Nostr deletion events using a list of objects and a passed
    adapter and publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager()
    pubkey = private_key.public_key.hex()

    for i in objs:

        obj = i.getObject() if ICatalogBrain.providedBy(i) else i

        converter = INostrEvent(obj)
        event = Event(kind=5, content="")
        a = f"{converter.kind()}:{pubkey}:{converter.uid()}"
        event.add_tag("a", a)

        client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager)

    return counter


def create_all_events():
    """Search for all supported objects, get metadata and send creation events to
    nostr
    """

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    result1 = create_events(brains1, INostrTimeBasedCalendarEvent)

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    result2 = create_events(brains2, INostrAmbEvent)

    msg = _("Events created or updated")
    msg = translate(msg, context=getRequest())

    return f"{result1+result2} {msg}"


def delete_all_events():
    """Search for all supported objects, get metadata and send deletion events to
    nostr
    """

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    result1 = delete_events(brains1, INostrTimeBasedCalendarEvent)

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    result2 = delete_events(brains2, INostrAmbEvent)

    msg = _("Events deleted")
    msg = translate(msg, context=getRequest())

    return f"{result1+result2} {msg}"
