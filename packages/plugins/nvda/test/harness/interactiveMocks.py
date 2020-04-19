import types

Fakes = types.SimpleNamespace()


def __setupMocks():
    __setupSpeechViewerMocks()


def __setupSpeechViewerMocks():
    from plugins.nvda.test.mocks.dependencies.speechViewerFakes import (
        createInteractiveFake,
    )

    import sys

    fakeSpeechViewerModule = createInteractiveFake()

    sys.modules["speechViewer"] = fakeSpeechViewerModule

    Fakes.SpeechViewer = fakeSpeechViewerModule


__setupMocks()
