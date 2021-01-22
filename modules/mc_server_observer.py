import socket
import time
from enum import IntEnum
from typing import Tuple, Optional

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse


class State(IntEnum):
    UNKNOWN = 0
    OFFLINE = 1
    ASSUMED_STARTING = 2
    PROVED_STARTING = 3
    ONLINE = 4
    ASSUMED_STOPPING = 5


class MCServerObserver:
    _cache_time__s = 10

    def __init__(self, server_address: str):
        """address from minecraft client as HOST:PORT"""
        self._last_reply = None
        self._last_fetched = 0
        self._server = MinecraftServer.lookup(server_address)

        self._assumed_starting_until = 0
        self._assumed_stopping_until = 0

    def assume_starting(self, seconds: int):
        """can't check that the server is starting until it actually answers any calls,
        assume so until proven by an answer or disproven when 'seconds' passed"""
        self._assumed_stopping_until = 0
        self._assumed_starting_until = time.time() + seconds

    def assume_stopping(self, seconds: int):
        """server will act like it is still online for a few seconds, assume it is stopping"""
        self._assumed_starting_until = 0
        self._assumed_stopping_until = time.time() + seconds

    def _fetch_state(self) -> PingResponse:
        """Caches results to reduce load, prevent bans and decrease latency for spammer clients"""
        now = time.time()
        if (now - self._last_fetched) < self._cache_time__s and self._last_reply is not None:
            # print("using cached value")
            return self._last_reply

        # print(f"Fetching status for {LOCAL_ADDRESS}")
        last_state = self._server.status()
        self._last_fetched = time.time()
        return last_state

    def is_online(self):
        # could also use try: server.ping(), but this is more comprehensive
        return self.get_state()[0] == State.ONLINE

    def get_state(self) -> Tuple[State, Optional[PingResponse]]:
        try:
            state = self._fetch_state()

            # try to get result first to see if offline is proven
            if self._assumed_stopping_until > time.time(): return State.ASSUMED_STOPPING, None

            return State.ONLINE, state
        except ConnectionRefusedError:
            # nothing there (yet?)
            if self._assumed_starting_until > time.time(): return State.ASSUMED_STARTING, None
            return State.OFFLINE, None
        except BrokenPipeError:
            # there, but unable to handle request
            return State.PROVED_STARTING, None

    def get_state_str(self) -> str:
        state, response = self.get_state()
        if state == State.ONLINE:
            return self._state_response_to_str(response)
        elif state == State.ASSUMED_STARTING:
            return "assumed to be starting"
        elif state == State.PROVED_STARTING:
            return "starting"
        elif state == State.ASSUMED_STOPPING:
            # nothing there
            return "assumed to be stopping"
        elif state == State.OFFLINE:
            # nothing there
            return "offline"
        else:
            return "unknown"

    @staticmethod
    def _state_response_to_str(status: PingResponse) -> str:
        s_players = f"{status.players.online}/{status.players.max}"
        return f"online with {s_players} players ({status.latency:.0f}ms)"

    def get_players(self) -> str:
        state, response = self.get_state()

        if state != State.ONLINE:
            return "unknown, server not online"

        try:
            # needs enable-query=true in server.properties and open and forwarded UDP port for full list
            all_players = self._server.query().players.names
            return str(all_players)
        except socket.timeout:
            # state always works (for newer servers), but won't expose everything
            print("query failed, query not enabled or UDP port not open?")
            some_players = response.players.sample
            return str(some_players + "..?")
