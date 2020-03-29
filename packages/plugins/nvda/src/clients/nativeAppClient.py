from rx.subject import Subject


class _NativeAppClient:
    def __init__(self):
        self.__speechStream = Subject()

    @property
    def speechStream(self):
        return self.__speechStream

    # TODO - add streams for other vitals checks.
    #      - Consumer to choose frequencies + pass location of files
    # - Is NVDA installed? Is the plugin installed?
    # - Is NVDA running?
    # - Is the speech viewer active?


def connectToNVDA():
    return _NativeAppClient()
