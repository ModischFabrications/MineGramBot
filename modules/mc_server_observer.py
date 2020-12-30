import socket
import time
from enum import IntEnum
from typing import Tuple, Optional

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse

from config import LOCAL_ADDRESS

cache_time__s = 10

server = MinecraftServer.lookup(LOCAL_ADDRESS)

last_state = None
last_fetched = 0


class State(IntEnum):
    UNKOWN = 0
    OFFLINE = 1
    STARTING = 2
    ONLINE = 3


# TODO: if verbose: send updates on change

def _fetch_state() -> PingResponse:
    global last_state, last_fetched
    now = time.time()
    if (now - last_fetched) < cache_time__s and last_state is not None:
        # print("using cached value")
        return last_state

    # print(f"Fetching status for {LOCAL_ADDRESS}")
    last_state = server.status()
    last_fetched = time.time()
    return last_state


def is_online():
    # could also use server.ping()
    return get_state()[0] == State.ONLINE


def get_state() -> Tuple[State, Optional[PingResponse]]:
    """always works for newer servers, but won't expose everything"""

    try:
        state = _fetch_state()
        return State.ONLINE, state
    except ConnectionRefusedError:
        # nothing there
        return State.OFFLINE, None
    except BrokenPipeError:
        # there, but unable to handle request
        return State.STARTING, None


def get_state_str() -> str:
    """always works for newer servers, but won't expose everything"""

    state, response = get_state()
    if state == State.ONLINE:
        return _response_to_str(response)
    elif state == State.STARTING:
        return "still starting"
    elif state == State.OFFLINE:
        # nothing there
        return "offline"
    else:
        return "unknown"


def _response_to_str(status: PingResponse) -> str:
    s_players = f"{status.players.online}/{status.players.max}"
    return f"online with {s_players} players ({status.latency:.0f}ms)"


def get_query():
    """needs query = enabled in server.properties and open UDP port, but exposes everything"""
    try:
        return server.query()
    except socket.timeout:
        # UDP port not open or server not there
        raise Exception("UDP port not open or server not there")

# result.raw['modinfo']['modList']

# query = server.query()
# query.players.names
