from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate

from eteaching.plone.nostrmetadatasync import _
from eteaching.plone.nostrmetadatasync.base import create_events, delete_events
from eteaching.plone.nostrmetadatasync.utils import is_published, suitable_adapter


def transition_event(context, event):
    """Listens to internal 'transition' events of plone cms"""

    adapter = suitable_adapter(context)
    published = is_published(context)

    if published and adapter:
        try:
            result = create_events([context], adapter)
            tmsg = _("Nostr event created because an object was published")
            tmsg = translate(tmsg, context=getRequest())
            tmsg = f"{result} {tmsg}"
        except Exception as e:
            tmsg = e

        api.portal.show_message(message=tmsg, request=getRequest())

    if not published and adapter:
        print("--->Delete (unpublished)")
        try:
            result = delete_events([context], adapter)
            tmsg = _("Nostr event deleted because an object was set to private")
            tmsg = translate(tmsg, context=getRequest())
            tmsg = f"{result} {tmsg}"
        except Exception as e:
            tmsg = e

        api.portal.show_message(message=tmsg, request=getRequest())

    return


def modified(context, event):
    """Listens to internal 'modified' and 'deleted' events of plone cms"""

    adapter = suitable_adapter(context)
    published = is_published(context)

    if published and adapter:
        print("---->Modify...")
        try:
            result = create_events([context], adapter)
            tmsg = _("Nostr event modified because an object was modified")
            tmsg = translate(tmsg, context=getRequest())
            tmsg = f"{result} {tmsg}"
        except Exception as e:
            tmsg = e

        api.portal.show_message(message=tmsg, request=getRequest())

    if not published and adapter:
        print("---->Deleted (modified)")
        try:
            result = delete_events([context], adapter)
            tmsg = _(
                "Nostr event deleted in modified action because an "
                "object was set to private"
            )
            tmsg = translate(tmsg, context=getRequest())
            tmsg = f"{result} {tmsg}"
        except Exception as e:
            tmsg = e

        api.portal.show_message(message=tmsg, request=getRequest())

    return


def deleted(context, event):
    """IObjectRemovedEvent"""

    adapter = suitable_adapter(context)

    if adapter:
        print("---> Delete (deleted)")
        try:
            result = delete_events([context], adapter)
            tmsg = _("Nostr event deleted because an object was deleted")
            tmsg = translate(tmsg, context=getRequest())
            tmsg = f"{result} {tmsg}"
        except Exception as e:
            tmsg = e

        api.portal.show_message(message=tmsg, request=getRequest())
