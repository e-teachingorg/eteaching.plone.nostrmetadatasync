import inspect

from DateTime import DateTime
from plone import api
from zope.component import adapter
from zope.interface import Interface, implementer

from eteaching.plone.nostrmetadatasync.adapters import base
from eteaching.plone.nostrmetadatasync.interfaces import INostrAmbEvent


@implementer(INostrAmbEvent)
@adapter(Interface)
class NostrAmbEvent(base.NostrEventMixin):
    """Interface for Nostr AMB Event that reads
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
            ("type", self.amb_type()),
            ("name", self._title()),
            ("description", self._description()),
            ("t", self.amb_keywords()),
            ("inLanguage", self.amb_in_language()),
            ("creator", self.amb_creator()),
            ("dateCreated", self.amb_date_created()),
            ("datePublished", self.amb_date_published()),
            ("dateModified", self.amb_date_modified()),
            ("r", self._url()),
            ("h", self._community_pubkeys()),
        )

        # Filter elements that are None
        filtered = tuple(item for item in tags if item[1] is not None)
        # Expand tuple values
        normalized = self._expand_tags(*filtered)

        return normalized

    def amb_type(self):
        return "LearningResource"

    def amb_keywords(self):
        return getattr(self.context, "subject", None)

    def amb_in_language(self):
        return getattr(self.context, "language", None)

    def amb_creator(self):
        creator_ids = getattr(self.context, "creators", None)
        creator_objs = []
        for creator_id in creator_ids:
            user = api.user.get(username=creator_id)
            if user:
                creator_name = user.getProperty("fullname")
            if creator_name:
                creator_objs.append({"name": creator_name})
            else:
                creator_objs.append({"name": creator_id})
        if creator_objs:
            return tuple(creator_objs)
        return None

    def amb_date_created(self):
        c = getattr(self.context, "created", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                return c().ISO8601()
        return None

    def amb_date_published(self):
        c = getattr(self.context, "effective", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                if c().year() > 2000:  # If there are invalid date entries
                    return c().ISO8601()
                else:
                    return self.amb_date_created()
        return None

    def amb_date_modified(self):
        c = getattr(self.context, "modified", None)
        if inspect.ismethod(c):
            if isinstance(c(), DateTime):
                return c().ISO8601()
        return None

    def _community_pubkeys(self):
        ca = api.portal.get_registry_record(
            "nostrmetadatasync-settings.communities_amb", default=None
        )
        return ca
