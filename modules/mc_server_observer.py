from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse

from config import LOCAL_ADDRESS

server = MinecraftServer.lookup(LOCAL_ADDRESS)

last_state = None


# TODO: if verbose: send updates on change

def is_online():
    try:
        global last_state
        last_state = server.status()
        return True
    except ConnectionRefusedError or BrokenPipeError:
        # nothing there
        return False


def get_status() -> str:
    """always works for newer servers, but won't expose everything"""
    print(f"Fetching status for {LOCAL_ADDRESS}")

    try:
        global last_state
        last_state = server.status()
        return status_to_str(last_state)
    except ConnectionRefusedError:
        # nothing there
        return "offline"
    except BrokenPipeError:
        # there, but unable to handle request
        return "still starting"


def status_to_str(status: PingResponse) -> str:
    s_players = f"{status.players.online}/{status.players.max}"
    return f"Online with {s_players} players ({status.latency}ms)"


def get_query():
    """needs query = enabled in server.properties, but exposes everything"""
    return server.query()


def get_players():
    return server.status().players

# query = server.query()
# query.players.names
