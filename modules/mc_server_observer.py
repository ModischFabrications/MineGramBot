from mcstatus import MinecraftServer

from config import LOCAL_ADDRESS

server = MinecraftServer.lookup(LOCAL_ADDRESS)


# TODO: if verbose: send updates on change

def get_status():
    """always works for newer servers, but won't expose everything"""
    print(f"Fetching status for {LOCAL_ADDRESS}")

    try:
        return server.status()
    except ConnectionRefusedError:
        return "Offline"


def get_query():
    """needs query = enabled in server.properties, but exposes everthing"""
    return server.query()


def get_players():
    return server.status().players

# query = server.query()
# query.players.names
