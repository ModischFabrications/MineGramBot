import threading
from typing import Callable

from config import MAX_TIME_TO_START__S
from modules.mc_server_observer import State, MCServerObserver


class MCServerObserverScheduler:
    _CHECK_WAIT_EVERY_S = 10
    _MAX_TRIES = MAX_TIME_TO_START__S / _CHECK_WAIT_EVERY_S

    def __init__(self, observer: MCServerObserver):
        self._observer = observer

    def call_when_online(self, on_success: Callable, on_timeout: Callable = lambda: None, tries_left: int = None):
        """Calls functions as soon as the minecraft server is online. Reentrancy not tested! """
        if tries_left is None: tries_left = self._MAX_TRIES - 1
        state = self._observer.get_state()[0]

        if state == State.ONLINE:
            # print("server online")
            on_success()
            return

        if state == State.PROVED_STARTING or state == State.ASSUMED_STARTING:
            if tries_left < 1:
                on_timeout()
                return
            # reschedule self, will probably lead to large stacks if running forever?
            threading.Timer(self._CHECK_WAIT_EVERY_S, self.call_when_online,
                            [on_success, on_timeout, tries_left - 1]).start()
            return

        on_timeout()
        raise RuntimeError(f"Server is {state.name}, it should have been starting")
