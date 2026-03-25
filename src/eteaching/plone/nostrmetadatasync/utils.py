
import os
from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
from eteaching.plone.nostrmetadatasync.interfaces import INostrTimeBasedCalendarEvent
from eteaching.plone.nostrmetadatasync.interfaces import INostrAmbEvent

import logging
from io import StringIO
from zope.interface.interfaces import ComponentLookupError


def login_details():

    try:
        relays = api.portal.get_registry_record(
                "nostrmetadatasync-settings.relays", default=None)
    except ComponentLookupError:
        return None

    private_key = os.environ.get("NOSTR_KEY")

    return {"relays": relays, "private_key": private_key}


def is_published(obj):
    """ Check if an object is published """

    try:
        state = api.content.get_state(obj)
    except WorkflowException:
        return False
    except api.exc.CannotGetPortalError:
        return False
    except api.exc.InvalidParameterError:
        return False
    if state == "published":
        return True
    return False


def get_registry_records():
    """ get necessary records from registry """

    try:

        cat = api.portal.get_registry_record(
                "nostrmetadatasync-settings.calendar_adapter_types",
                default=None)
        csp = api.portal.get_registry_record(
                "nostrmetadatasync-settings.calendar_search_params",
                default=None)
        aat = api.portal.get_registry_record(
                "nostrmetadatasync-settings.amb_adapter_types",
                default=None)
        asp = api.portal.get_registry_record(
                "nostrmetadatasync-settings.amb_search_params",
                default=None)

    except ComponentLookupError:

        return {"calendar_adapter_types": [], "calendar_search_params": "",
                "amb_adapter_types": [], "amb_search_params": ""}

    return {"calendar_adapter_types": cat, "calendar_search_params": csp,
            "amb_adapter_types": aat, "amb_search_params": asp}


def parse_filters(s):
    """ Parse filters from a given string in a list of lists"""

    def cast(v):
        if v == "True":
            return True
        if v == "False":
            return False
        try:
            return int(v)
        except Exception:
            pass
        try:
            return float(v)
        except Exception:
            pass
        return v  # String

    result = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = [x.strip() for x in part.split("=", 1)]
            result.setdefault(k, []).append(cast(v))

    out = []
    for k, vals in result.items():
        if len(vals) > 1:
            out.append([k, vals])
        else:
            v = vals[0]
            out.append([k, [v]] if isinstance(
                    v, (int, float)) and not isinstance(v, bool) else [k, v])
    return out


def check_obj(obj, p_type, s_params):
    """ Checks whether the given object is valid with regard to the
        given portal types and filters.
    """
    if p_type:
        # Supported portal type?
        if obj.portal_type in p_type:
            # Are there any other filters?
            if s_params:
                filters = parse_filters(s_params)
                # for every single filter
                for f in filters:
                    obj_value = getattr(obj, f[0], None)
                    # Does the object have such an attribute?
                    if obj_value:
                        if isinstance(obj_value, list):
                            # Is the attribute value in the list?
                            if f[1] in obj_value:
                                return True
                        elif isinstance(obj_value, str):
                            # Is the attribute value equal to the string?
                            if f[1] == obj_value:
                                return True
            else:
                # If portal type and no other Filters
                return True
        else:
            # If no supported portal type
            return False
    # If no portal type
    return False


def suitable_adapter(obj):
    """ Return the appropriate adapter based on the portal type. """

    registry_records = get_registry_records()

    cat = registry_records["calendar_adapter_types"]
    csp = registry_records["calendar_search_params"]
    aat = registry_records["amb_adapter_types"]
    asp = registry_records["amb_search_params"]

    check1 = check_obj(obj, cat, csp)
    if check1:
        return INostrTimeBasedCalendarEvent
    check2 = check_obj(obj, aat, asp)
    if check2:
        return INostrAmbEvent

    return False


def get_brains(portal_types, search_params):
    """ Return catalog brains for given portal type and search parameters """

    catalog = api.portal.get_tool("portal_catalog")
    cf = {}

    p = api.portal.get_registry_record(portal_types, default=None)
    if not p:
        return []
    s = api.portal.get_registry_record(search_params, default=None)

    f = parse_filters(s)
    for i in f:
        cf[i[0]] = i[1]
    cf["portal_type"] = p

    return catalog(cf)


def capture_pynostr_warnings(func):
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.WARNING)

    logger = logging.getLogger("pynostr")
    logger.addHandler(handler)

    try:
        func()
    finally:
        logger.removeHandler(handler)

    return stream.getvalue().strip() or None


def normalize_tags(tags):
    result = []
    for key, value in tags:
        if isinstance(value, tuple):
            for v in value:
                result.append((key, v))
        else:
            result.append((key, value))
    return tuple(result)
