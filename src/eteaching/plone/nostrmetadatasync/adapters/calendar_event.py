import pytz
from plone import api
from zope.component import adapter
from zope.interface import Interface, implementer

from eteaching.plone.nostrmetadatasync.adapters import base
from eteaching.plone.nostrmetadatasync.interfaces import (
    INostrTimeBasedCalendarEvent
)


@implementer(INostrTimeBasedCalendarEvent)
@adapter(Interface)
class NostrTimeBasedCalendarEvent(base.NostrEventMixin):
    """Adapter for Nostr Date-Based or Time-Based Calendar Event that reads
    its data from a Plone event object (plone.app.event).

    Kind Number: 31922 (Date-Based) / 31923 (Time-Based)
    Event Range: Addressable
    Defined in: NIP-52
    URL: https://nostrbook.dev/kinds/31922
         https://nostrbook.dev/kinds/31923

    // Usage with pynostr

    from pynostr.event import Event
    from eteaching.plone.nostrmetadatasync.interfaces import
                                INostrTimeBasedCalendarEvent

    calendar_event = INostrTimeBasedCalendarEvent(PloneEvent)
    tags = calendar_event.tags()
    content = calendar_event.content()
    kind = calendar_event.kind

    nostr_event = Event(kind=kind, content=content, tags=tags)
    """

    def __init__(self, context):
        self.context = context
        self.tz_start = self._tz_datetime(self.context.start)
        self.tz_end = self._tz_datetime(self.context.end)

    def kind(self):
        if getattr(self.context, "whole_day", False):
            return 31922
        return 31923

    def tags(self):
        tags = (
            ("d", self.uid()),
            ("title", self._title()),
            ("summary", self._description()),
            ("start", self._start()),
            ("end", self._end()),
            ("start_tzid", self._start_tzid()),
            ("end_tzid", self._end_tzid()),
            ("r", self._url()),
            ("h", self._community_pubkeys()),
        )

        # Filter elements that are None
        filtered = tuple(item for item in tags if item[1] is not None)
        # Expand tuple values
        normalized = self._expand_tags(*filtered)

        return normalized

    def _start(self):
        if (
            getattr(self.context, "whole_day", False)
            and self.tz_start
        ):
            return str(self.context.start.date().isoformat())
        return str(int(self.tz_start.timestamp()))  # to unix seconds

    def _end(self):
        if (
            getattr(self.context, "whole_day", False)
            and self.tz_end
            and not getattr(self.context, "open_end", False)
        ):
            return str(self.context.end.date().isoformat())
        if (
            not getattr(self.context, "open_end", False)
            and self.tz_end
            and self.tz_end > self.tz_start
        ):
            return str(int(self.tz_end.timestamp()))  # to unix seconds
        return None

    def _start_tzid(self):
        if getattr(self.context, "whole_day", False):
            return None
        return self.tz_start.tzinfo.zone

    def _end_tzid(self):
        if getattr(self.context, "whole_day", False):
            return None
        if (
            not getattr(self.context, "open_end", False)
            and self.tz_end
            and self.tz_end > self.tz_start
        ):
            return self.tz_end.tzinfo.zone
        return None

    def _tz_datetime(self, dt):
        if not dt:
            return None
        if dt.tzinfo is None:
            ptz = api.portal.get_registry_record("plone.portal_timezone")
            ptz = pytz.timezone(ptz)
            dt = dt.astimezone(ptz)
        return dt

    def _community_pubkeys(self):
        ca = api.portal.get_registry_record(
            "nostrmetadatasync-settings.communities_calendar", default=None
        )
        return ca
