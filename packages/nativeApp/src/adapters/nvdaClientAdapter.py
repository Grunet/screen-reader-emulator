from plugins.nvda.src.clients.nativeAppClient import connectToNVDA


class _NVDAClientAdapter:
    def __init__(self, nvdaClient):
        self.__nvdaClient = nvdaClient

        # TODO - Merge all of the client's streams together
        #      - into a single stream of JSON

    @property
    def outputStream(self):
        return self.__nvdaClient.speechStream


def createConnectionToNVDA():
    nvdaClient = connectToNVDA()

    return _NVDAClientAdapter(nvdaClient)
