from pynostr.key import PrivateKey
from pynostr.relay_manager import RelayManager

from eteaching.plone.nostrmetadatasync.utils import (
    capture_pynostr_warnings,
    login_details,
)


def init_relay_manager():
    """Reads credentials and initializes the relay manager for Nostr"""

    cred = login_details()

    relay_manager = RelayManager(timeout=1)

    for relay in cred["relays"]:
        relay_manager.add_relay(relay)

    private_key = PrivateKey.from_nsec(cred["private_key"])

    return relay_manager, private_key


def publish_event(relay_manager, private_key, event):
    """Sign nostr events and publish them"""

    event.sign(private_key.hex())
    relay_manager.publish_event(event)


def sync_events(relay_manager):
    """Sync a actions with the relay, get, count and return ok notices"""

    msg = capture_pynostr_warnings(lambda: relay_manager.run_sync())
    if msg:
        raise Exception(f"[NOSTR] {msg}")

    counter = 0

    while relay_manager.message_pool.has_ok_notices():
        ok_msg = relay_manager.message_pool.get_ok_notice()
        print(ok_msg)
        counter += 1
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        print(event_msg.event.to_dict())

    return counter
