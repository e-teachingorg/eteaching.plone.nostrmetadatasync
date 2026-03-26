
import os
from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
from eteaching.plone.nostrmetadatasync.interfaces import INostrTimeBasedCalendarEvent
from eteaching.plone.nostrmetadatasync.interfaces import INostrAmbEvent

import logging
from io import StringIO
from zope.globalrequest import getRequest
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
    catalog = api.portal.get_tool("portal_catalog")
    filters = parse_filters(s_params)
    cf = {}

    cf["portal_type"] = p_type
    cf["UID"] = obj.UID()

    for entry in filters:
        cf[entry[0]] = entry[1]

    brains = catalog(cf)

    return True if len(brains) == 1 else False


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
    """Capture warnings from pynostr module"""
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
    """Normalize ((key, (value1, value2))) to
       ((key, value1), (key, value2))"""
    result = []
    for key, value in tags:
        if isinstance(value, tuple):
            for v in value:
                result.append((key, v))
        else:
            result.append((key, value))
    return tuple(result)


def replace_base_url(url):
    """ Replace Request URL3 by base_url from registry """
    url3 = getRequest()["URL3"]
    bu = api.portal.get_registry_record(
            "nostrmetadatasync-settings.base_url",
            default=None)
    if bu:
        return(url.replace(url3, bu))
    return url
