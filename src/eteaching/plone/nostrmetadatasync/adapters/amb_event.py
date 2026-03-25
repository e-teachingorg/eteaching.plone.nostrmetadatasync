
import hashlib
import inspect

from DateTime import DateTime
from plone import api
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter

from eteaching.plone.nostrmetadatasync.interfaces import INostrAmbEvent
from eteaching.plone.nostrmetadatasync.utils import normalize_tags,\
    replace_base_url


@implementer(INostrAmbEvent)
@adapter(Interface)
class NostrAmbEvent:
    """ Interface for Nostr AMB Event that reads
        its data from a Plone type.

        Kind Number: 30142
        Defined in: NIP-AMB
        https://nostrhub.edufeed.org/naddr1qvzqqqrcvypzp0wzr7fmrcktw4sgemxh5zsq5auh08vnvlwf0x9anusn7pkft0zgqy2hwumn8ghj7un9d3shjtnyd968gmewwp6kyqqtv4j82en9v4jz6ctdvgy0cnas

        // Usage with pynostr

        from pynostr.event import Event
        from eteaching.plone.nostrmetadatasync.interfaces import
                                    INostrAmbEvent

        amb_event = INostrAmbEvent(AMBSupportedType)
        tags = amb_event.tags()
        content = amb_event.content()
        kind = amb_event.kind

        nostr_event = Event(kind=kind, content=content, tags=tags)
    """

    def __init__(self, context):
        self.context = context

    def kind(self):
        return 30142

    def tags(self):
        tags = (
            ("d", self.uid()),
            ("name", self._name()),
            ("description", self._description()),
            ("t", self._keywords()),
            ("inLanguage", self._in_language()),
            ("creator:name", self._creator_name()),
            ("dateCreated", self._date_created()),
            ("datePublished", self._date_published()),
            ("dateModified", self._date_modified()),
            ("r", self._url())
        )

        # Filter elements that are None
        filtered = tuple(item for item in tags if item[1] is not None)
        # Normalize tuple values
        normalized = normalize_tags(filtered)

        return normalized

    def content(self):
        return self.context.description

    def uid(self):
        s = self.context.UID()
        return hashlib.sha256(s.encode()).hexdigest()

    def _name(self):
        return self.context.title

    def _description(self):
        return self.context.description

    def _keywords(self):
        return getattr(self.context, "subject", None)

    def _in_language(self):
        return getattr(self.context, "language", None)

    def _creator_name(self):
        creator_ids = getattr(self.context, "creators", None)
        creator_names = []
        for creator in creator_ids:
            user = api.user.get(username=creator)
            name = user.getProperty('fullname')
            if name:
                creator_names.append(name)
            else:
                creator_names.append(creator)
        if creator_names:
            return tuple(creator_names)
        return None

    def _date_created(self):
        c = getattr(self.context, "created", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                return c().ISO8601()
        return None

    def _date_published(self):
        c = getattr(self.context, "effective", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                if c().year() > 2000:  # If there are invalid date entries
                    return c().ISO8601()
                else:
                    return self._date_created()
        return None

    def _date_modified(self):
        c = getattr(self.context, "modified", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                return c().ISO8601()
        return None

    def _url(self):
        url = self.context.absolute_url()
        return replace_base_url(url)
