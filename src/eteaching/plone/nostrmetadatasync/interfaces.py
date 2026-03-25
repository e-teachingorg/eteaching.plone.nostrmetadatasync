"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from eteaching.plone.nostrmetadatasync import _


class IEteachingPloneNostrmetadatasyncLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INostrMetadataSyncSettings(Interface):
    """ Interface for Nostr MetadataSync Settings """

    base_url = schema.TextLine(
        title=_("label_base_url",
                default="Base URL"),
        description=_("help_base_url",
                      default="Custom base URL with domain and page root "
                      "(e.g. https://www.e-teaching.org). If you enter a "
                      "value here, it will replace the base URL in all sent "
                      "URLs, such as http://localhost:8080/Plone. This allows "
                      "you to test the add-on locally."),
        default="",
        missing_value="",
        required=False,
    )

    relays = schema.Tuple(
        title=_("label_relays", default="Relays"),
        description=_(
                "help_relays",
                default="One relay per line (e.g. ws://localhost:10547)"),
        value_type=schema.TextLine(),
        required=True,
    )

    calendar_adapter_types = schema.List(
        title=_("label_calendar_adapter_types",
                default="Calendar adapter types"),
        description=_("help_calendar_adapter_types",
                      default="All content types for which the calendar "
                      "adapter is to be used are added here."),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        ),
        required=False,
    )

    calendar_search_params = schema.TextLine(
        title=_("label_calendar_search_params",
                default="Event query parameters"),
        description=_("help_calendar_search_params",
                      default="Additional query parameter for calendar event "
                      "content (e.g. key1=value1;key2=value2;key1=value3)"),
        default="",
        missing_value="",
        required=False,
    )

    amb_adapter_types = schema.List(
        title=_("label_amb_adapter_types",
                default="AMB adapter types"),
        description=_("help_amb_adapter_types",
                      default="All content types for which the AMB "
                      "adapter is to be used are added here."),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        ),
        required=False,
    )

    amb_search_params = schema.TextLine(
        title=_("label_amb_search_params",
                default="AMB query parameters"),
        description=_("help_amb_search_params",
                      default="Additional query parameter for AMB content "
                      "(e.g. key1=value1;key2=value2;key1=value3)"),
        default="",
        missing_value="",
        required=False,
    )


class INostrTimeBasedCalendarEvent(Interface):
    """ Interface for Nostr Time-Based Calendar Event that reads
        its data from a Plone event object.

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


class INostrAmbEvent(Interface):
    """ Interface for Nostr AMB Event that reads
        its data from a Plone AMB supported type.

        Kind Number: 31923
        Event Range: Addressable
        Defined in: NIP-23
        https://nostrbook.dev/kinds/30023

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
