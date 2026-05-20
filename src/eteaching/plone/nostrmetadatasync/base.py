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


all_events_timeout = 7


# def create_events(objs, INostrEvent, timeout):
def create_events(event_sets, timeout):
    """Creates Nostr events using a list of objects and a passed adapter and
    publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager(timeout)

    for event_set in event_sets:
        for count, i in enumerate(event_set["brains"]):

            obj = i.getObject() if ICatalogBrain.providedBy(i) else i

            n = event_set["adapter"](obj)
            event = Event(kind=n.kind(), content=n.content(), tags=n.tags())
            client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager, count)

    for relay in relay_manager.relays.values():
        relay.close()

    return counter


# def delete_events(objs, INostrEvent, timeout):
def delete_events(event_sets, timeout):
    """Creates Nostr deletion events using a list of objects and a passed
    adapter and publishes them on a relay."""

    relay_manager, private_key = client.init_relay_manager(timeout)
    pubkey = private_key.public_key.hex()

    for event_set in event_sets:
        for count, i in enumerate(event_set["brains"]):

            obj = i.getObject() if ICatalogBrain.providedBy(i) else i

            n = event_set["adapter"](obj)
            event = Event(kind=5, content="")
            a = f"{n.kind()}:{pubkey}:{n.uid()}"
            event.add_tag("a", a)

            client.publish_event(relay_manager, private_key, event)

    counter = client.sync_events(relay_manager, count)

    for relay in relay_manager.relays.values():
        relay.close()

    return counter


def create_all_events():
    """Search for all supported objects, get metadata and send creation events to
    nostr
    """

    event_sets = []

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    if brains1:
        event_sets.append({"brains": brains1,
                           "adapter": INostrTimeBasedCalendarEvent})

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    if brains2:
        event_sets.append({"brains": brains2,
                           "adapter": INostrAmbEvent})

    result = create_events(event_sets, all_events_timeout)

    msg = _("Events created or updated")
    msg = translate(msg, context=getRequest())

    return f"{result} {msg}"


def delete_all_events():
    """Search for all supported objects, get metadata and send deletion events to
    nostr
    """

    event_sets = []

    brains1 = get_brains(
        "nostrmetadatasync-settings.calendar_adapter_types",
        "nostrmetadatasync-settings.calendar_search_params",
    )
    if brains1:
        event_sets.append({"brains": brains1,
                           "adapter": INostrTimeBasedCalendarEvent})

    brains2 = get_brains(
        "nostrmetadatasync-settings.amb_adapter_types",
        "nostrmetadatasync-settings.amb_search_params",
    )
    if brains2:
        event_sets.append({"brains": brains2,
                           "adapter": INostrAmbEvent})

    result = create_events(event_sets, all_events_timeout)

    msg = _("Events deleted")
    msg = translate(msg, context=getRequest())

    return f"{result} {msg}"
