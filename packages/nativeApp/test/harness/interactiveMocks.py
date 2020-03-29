import types

Fakes = types.SimpleNamespace()


def __setupMocks():
    __setupStdinMocks()
    __setupNvdaClientMocks()


def __setupStdinMocks():
    from nativeApp.test.mocks.dependencies.stdinMocks import (
        mockStdinBuffer,
        sendMessageToStdin,
    )

    mockStdinBuffer()

    Fakes.Stdin = types.SimpleNamespace()
    Fakes.Stdin.on_next = sendMessageToStdin  # Not an actual Rx observer/subject


def __setupNvdaClientMocks():
    import plugins.nvda.test.mocks.src.clients.nativeAppClientFakes

    import sys

    sys.modules[
        "plugins.nvda.src.clients.nativeAppClient"
    ] = plugins.nvda.test.mocks.src.clients.nativeAppClientFakes

    Fakes.NvdaClient = (
        plugins.nvda.test.mocks.src.clients.nativeAppClientFakes.interactiveFake
    )


__setupMocks()
