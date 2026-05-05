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


def create_events(objs, INostrEvent, timeout):
    """Creates Nostr events using a list of objects and a passed adapter and
    publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager(timeout)
    
    for count, i in enumerate(objs):

        obj = i.getObject() if ICatalogBrain.providedBy(i) else i

        n = INostrEvent(obj)
        event = Event(kind=n.kind(), content=n.content(), tags=n.tags())
        client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager, count)

    return counter


def delete_events(objs, INostrEvent, timeout):
    """Creates Nostr deletion events using a list of objects and a passed
    adapter and publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager(timeout)
    pubkey = private_key.public_key.hex()

    for count, i in enumerate(objs):

        obj = i.getObject() if ICatalogBrain.providedBy(i) else i

        n = INostrEvent(obj)
        event = Event(kind=5, content="")
        a = f"{n.kind()}:{pubkey}:{n.uid()}"
        event.add_tag("a", a)

        client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager, count)

    return counter


def create_all_events():
    """Search for all supported objects, get metadata and send creation events to
    nostr
    """
    
    result1 = 0
    result2 = 0

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    if brains1:
        result1 = create_events(brains1, INostrTimeBasedCalendarEvent, 6)

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    if brains2:
        result2 = create_events(brains2, INostrAmbEvent, 6)

    msg = _("Events created or updated")
    msg = translate(msg, context=getRequest())

    return f"{result1+result2} {msg}"


def delete_all_events():
    """Search for all supported objects, get metadata and send deletion events to
    nostr
    """

    result1 = 0
    result2 = 0

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    if brains1:
        result1 = delete_events(brains1, INostrTimeBasedCalendarEvent, 6)

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    if brains2:
        result2 = delete_events(brains2, INostrAmbEvent, 6)

    msg = _("Events deleted")
    msg = translate(msg, context=getRequest())

    return f"{result1+result2} {msg}"
