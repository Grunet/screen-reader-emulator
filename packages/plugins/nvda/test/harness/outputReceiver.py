from multiprocessing.connection import Client

from plugins.nvda.src.commConstants import address, authkey

# This will throw an exception if the plugin hasn't setup the Listener yet
conn = Client(address, authkey=authkey)

while True:
    output = conn.recv()

    print(output)
