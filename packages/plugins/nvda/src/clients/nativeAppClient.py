from multiprocessing.connection import Client

import asyncio
from rx.subject import Subject
from rx.operators import map, with_latest_from, merge

from plugins.nvda.src.commConstants import OutputKeys
from plugins.nvda.src.plugin import rehydrateMessage
from plugins.nvda.src.commConstants import _address, _authkey

_NVDA_EXPECTED_STARTUP_TIME = 2
_PADDING_FOR_NVDA_STARTUP_TIME = 1


class _NativeAppClient:
    def __init__(self):
        self.__rawPluginOutputStream = Subject()
        self.__rawPluginOutputStream.pipe(
            map(lambda dehydratedMsgDict: rehydrateMessage(dehydratedMsgDict))
        )

        self.__connectionStatusStream = Subject()

        self.__speechStream = with_latest_from(
            self.__rawPluginOutputStream, self.__connectionStatusStream
        ).pipe(
            map(lambda combinedTuple: {**combinedTuple[0], **combinedTuple[1]}),
            merge(self.__connectionStatusStream),
        )

        # TODO - need to trigger NVDA to startup, if it isn't already
        #      - first need to check if NVDA is installed + if the plugin is

        asyncio.create_task(self.__startListeningForOutput())

    @property
    def speechStream(self):
        return self.__speechStream

    # TODO - add streams for other vitals checks.
    #      - Consumer to choose frequencies?
    # - Is NVDA running?

    async def __startListeningForOutput(self):
        await self.__connectToOutputServer()

        asyncio.create_task(self.__pollForOutput())

    async def __connectToOutputServer(self):
        self.__serverConnection = None  # Remove a potential previous, broken connection

        await asyncio.sleep(
            _NVDA_EXPECTED_STARTUP_TIME + _PADDING_FOR_NVDA_STARTUP_TIME
        )

        while True:
            try:
                self.__serverConnection = Client(
                    _address, _authkey
                )  # Seems to wait ~3s before exception is raised

                self.__connectionStatusStream.on_next({OutputKeys.IS_CONNECTED: True})
                break

            except ConnectionRefusedError:  # If the listener hasn't been setup yet
                self.__connectionStatusStream.on_next({OutputKeys.IS_CONNECTED: False})

                await asyncio.sleep(0)

    async def __pollForOutput(self):
        while True:
            if self.__serverConnection and self.__serverConnection.poll():
                try:
                    dehydratedMsgDict = self.__serverConnection.recv()
                    self.__rawPluginOutputStream.on_next(dehydratedMsgDict)

                except ConnectionResetError:  # If NVDA/the plugin is terminated
                    self.__connectionStatusStream.on_next(
                        {OutputKeys.IS_CONNECTED: False}
                    )

                    await self.__connectToOutputServer()  # In case it restarts
            else:
                await asyncio.sleep(0)


def connectToNVDA():
    return _NativeAppClient()
