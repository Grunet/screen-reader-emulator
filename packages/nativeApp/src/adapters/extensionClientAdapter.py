from extension.background.src.clients.nativeClient import connectToExtension


class _ExtensionClientAdapter:
    def __init__(self, extensionClient):
        self.__extensionClient = extensionClient

    @property
    def inputStream(self):
        return self.__extensionClient.inputStream

    @property
    def outputStream(self):
        return self.__extensionClient.outputStream


def createConnectionToExtension(nativeAppStdin, nativeAppStdout):
    extensionClient = connectToExtension(nativeAppStdin, nativeAppStdout)

    return _ExtensionClientAdapter(extensionClient)
