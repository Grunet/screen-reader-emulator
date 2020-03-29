# To hit breakpoints set in VS Code later on
# breakpoint()  # 0) Uncomment this
# 1) Run the harness from the tasks.json task
# 2) Use the Python launch.json debug config to attach to this process
# 3) Then type the keyword "continue" at the PDB prompt


from threading import Thread


# Setting up mocks
from nativeApp.test.mocks.dependencies.stdinMocks import (  # noqa
    mockStdinBuffer,
    sendMessageToStdin,  # Use this to simulate input to the nativeApp from the browser
)

mockStdinBuffer()

import plugins.nvda.test.mocks.src.clients.nativeAppClientFakes

import sys

sys.modules[
    "plugins.nvda.src.clients.nativeAppClient"
] = plugins.nvda.test.mocks.src.clients.nativeAppClientFakes

import types

Fakes = types.SimpleNamespace()
Fakes.Stdin = types.SimpleNamespace()
Fakes.Stdin.on_next = sendMessageToStdin  # Not an actual Rx observer/subject
Fakes.NvdaClient = (
    plugins.nvda.test.mocks.src.clients.nativeAppClientFakes.interactiveFake
)

# Running the nativeApp in a separate thread to allow for interactive input
def __runApp():
    import runpy

    runpy.run_module("nativeApp.src.app")


t = Thread(target=__runApp)
t.daemon = True
t.start()
