import socket
import time
from enum import IntEnum
from typing import Tuple, Optional

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse


class State(IntEnum):
    UNKOWN = 0
    OFFLINE = 1
    STARTING = 2
    ONLINE = 3


class MCServerObserver:
    _cache_time__s = 10

    def __init__(self, local_address):
        self._last_state = None
        self._last_fetched = 0
        self._server = MinecraftServer.lookup(local_address)

    def _fetch_state(self) -> PingResponse:
        now = time.time()
        if (now - self._last_fetched) < self._cache_time__s and self._last_state is not None:
            # print("using cached value")
            return self._last_state

        # print(f"Fetching status for {LOCAL_ADDRESS}")
        last_state = self._server.status()
        last_fetched = time.time()
        return last_state

    def is_online(self):
        # could also use server.ping()
        return self.get_state()[0] == State.ONLINE

    def get_state(self) -> Tuple[State, Optional[PingResponse]]:
        """always works for newer servers, but won't expose everything"""

        try:
            state = self._fetch_state()
            return State.ONLINE, state
        except ConnectionRefusedError:
            # nothing there
            return State.OFFLINE, None
        except BrokenPipeError:
            # there, but unable to handle request
            return State.STARTING, None

    def get_state_str(self) -> str:
        """always works for newer servers, but won't expose everything"""

        state, response = self.get_state()
        if state == State.ONLINE:
            return self._response_to_str(response)
        elif state == State.STARTING:
            return "starting"
        elif state == State.OFFLINE:
            # nothing there
            return "offline"
        else:
            return "unknown"

    @staticmethod
    def _response_to_str(status: PingResponse) -> str:
        s_players = f"{status.players.online}/{status.players.max}"
        return f"online with {s_players} players ({status.latency:.0f}ms)"

    def get_query(self):
        """needs query = enabled in server.properties and open UDP port, but exposes everything"""
        try:
            return self._server.query()
        except socket.timeout:
            # UDP port not open or server not there
            raise Exception("UDP port not open or server not there")

    # result.raw['modinfo']['modList']

    # query = server.query()
    # query.players.names
