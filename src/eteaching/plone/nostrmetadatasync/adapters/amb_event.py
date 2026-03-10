
import hashlib

from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter

from eteaching.plone.nostrmetadatasync.interfaces import INostrAmbEvent


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
        return (
            ("d", self.uid()),
            ("name", self._name()),
            ("description", self._description()),
        )

    def content(self):
        return self.context.description

    def uid(self):
        s = self.context.UID()
        return hashlib.sha256(s.encode()).hexdigest()

    def _name(self):
        return self.context.title

    def _description(self):
        return self.context.description
