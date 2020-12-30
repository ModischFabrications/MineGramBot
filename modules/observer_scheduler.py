import threading
from typing import Callable

from modules.mc_server_observer import State, MCServerObserver


class MCServerObserverScheduler:
    _CHECK_WAIT_S = 10
    _MAX_TRIES = (5 * 60) / _CHECK_WAIT_S

    def __init__(self, observer: MCServerObserver):
        self._observer = observer

    def call_when_online(self, on_success: Callable, on_timeout: Callable = lambda: None, tries_left: int = None):
        """Call as soon as the minecraft server is online. Reentrancy not tested! """
        if tries_left is None: tries_left = self._MAX_TRIES - 1
        state = self._observer.get_state()[0]
        # state = State.STARTING

        if state == State.ONLINE:
            # print("server online")
            on_success()
            return

        if state == State.STARTING:
            if tries_left < 1:
                on_timeout()
                return
            # print("rescheduled call_when_online")
            threading.Timer(self._CHECK_WAIT_S, self.call_when_online, [on_success, on_timeout, tries_left - 1]).start()
            return

        on_timeout()
        raise RuntimeError(f"Server is {state.name}, starting was expected")
