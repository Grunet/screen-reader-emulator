from multiprocessing.connection import Client
from pprint import pprint

from plugins.nvda.src.commConstants import _address, _authkey

# This will throw an exception if the plugin hasn't setup the Listener yet
conn = Client(_address, authkey=_authkey)

while True:
    output = conn.recv()

    pprint(output, width=1)  # Wraps lines of a dictionary
