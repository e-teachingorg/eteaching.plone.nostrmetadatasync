import hashlib

from plone import api
import pytz
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter

from eteaching.plone.nostrmetadatasync.interfaces import INostrTimeBasedCalendarEvent

from zope.component import getGlobalSiteManager


@implementer(INostrTimeBasedCalendarEvent)
@adapter(Interface)
class NostrTimeBasedCalendarEvent:
    """ Adapter for Nostr Time-Based Calendar Event that reads
        its data from a Plone event object (plone.app.event).

        Kind Number: 31923
        Event Range: Addressable
        Defined in: NIP-52
        URL: https://nostrbook.dev/kinds/31923

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
        return 31923

    def tags(self):
        return (
            ("d", self.uid()),
            ("title", self._title()),
            ("summary", self._sumary()),
            ("start", str(self._start())),
            ("end", str(self._end())),
            ("start_tzid", self._start_tzid()),
            ("end_tzid", self._end_tzid()),
            ("r", self._event_url())
        )

    def content(self):
        return self.context.description

    def uid(self):
        s = self.context.UID()
        return hashlib.sha256(s.encode()).hexdigest()

    def _title(self):
        return self.context.title

    def _sumary(self):
        return self.context.description

    def _start(self):
        return int(self.tz_start.timestamp())  # to unix seconds

    def _end(self):
        if (
                not getattr(self.context, "open_end", False)
                and self.tz_end
                and self.tz_end > self.tz_start):
            return int(self.tz_end.timestamp())  # to unix seconds
        return ""

    def _start_tzid(self):
        return self.tz_start.tzinfo.zone

    def _end_tzid(self):
        if (
                not getattr(self.context, "open_end", False)
                and self.tz_end
                and self.tz_end > self.tz_start):
            return self.tz_end.tzinfo.zone
        return ""

    def _event_url(self):

        url = self.context.absolute_url()
        # for local testing
        et = "https://www.e-teaching.org"
        lo = "http://localhost:7080/eteaching"
        return url.replace(lo, et)

    def _tz_datetime(self, dt):
        if not dt:
            return None
        if dt.tzinfo is None:
            ptz = api.portal.get_registry_record("plone.portal_timezone")
            ptz = pytz.timezone(ptz)
            dt = dt.astimezone(ptz)
        return dt
