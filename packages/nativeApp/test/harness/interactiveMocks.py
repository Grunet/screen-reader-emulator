
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