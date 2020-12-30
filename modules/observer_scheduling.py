import threading
from typing import Callable

from modules.mc_server_observer import State, get_state

CHECK_WAIT_S = 10
MAX_TRIES = (.5 * 60) / CHECK_WAIT_S


def call_when_online(on_success: Callable, on_timeout: Callable = lambda: None, tries_left: int = None):
    """Call as soon as the minecraft server is online. Reentrancy not tested! """
    if tries_left is None: tries_left = MAX_TRIES - 1
    state = get_state()[0]
    # state = State.STARTING

    if state == State.ONLINE:
        print("server online")
        on_success()
        return

    if state == State.STARTING:
        if tries_left < 1:
            on_timeout()
            return
        print("rescheduled call_when_online")
        threading.Timer(CHECK_WAIT_S, call_when_online, [on_success, on_timeout, tries_left - 1]).start()
        return

    on_timeout()
    raise RuntimeError(f"Server is {state.name}, starting was expected")
