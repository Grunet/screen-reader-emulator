from rx.subject import Subject

import json
import struct
import asyncio


class _StandardStreamsToRxStreamsAdapter:
    def __init__(self, stdin, stdout):
        self.__stdinOfApp = stdin
        self.__stdoutOfApp = stdout

        self.__inputStream = Subject()
        self.__inputStream.subscribe(on_next=lambda msg: self.__reactToInput(msg))

        self.__outputStream = Subject()  # Could this be a normal Observable somehow?
        asyncio.create_task(self.__pollForOutput())

    @property
    def inputStream(self):
        return self.__inputStream

    @property
    def outputStream(self):
        return self.__outputStream

    def __reactToInput(self, messageContent):
        self.__sendMessage(self.__encodeMessage(messageContent))

    def __encodeMessage(self, messageContent):
        encodedContent = json.dumps(messageContent).encode("utf-8")
        encodedLength = struct.pack("@I", len(encodedContent))
        return {"length": encodedLength, "content": encodedContent}

    def __sendMessage(self, encodedMessage):
        self.__stdoutOfApp.buffer.write(encodedMessage["length"])
        self.__stdoutOfApp.buffer.write(encodedMessage["content"])
        self.__stdoutOfApp.buffer.flush()

    async def __pollForOutput(self):
        while True:
            decodedOutput = await self.__getAndDecodeOutput()

            if decodedOutput:
                self.__outputStream.on_next(decodedOutput)

    async def __getAndDecodeOutput(self):
        rawLength = await asyncio.get_running_loop().run_in_executor(
            None, self.__doBlockingReadFromStdin
        )

        if len(rawLength) == 0:
            return None

        messageLength = struct.unpack("@I", rawLength)[0]
        message = self.__stdinOfApp.buffer.read(messageLength).decode("utf-8")

        return json.loads(message)

    def __doBlockingReadFromStdin(self):
        return self.__stdinOfApp.buffer.read(4)


def convertStdToRxStreams(stdin, stdout):
    return _StandardStreamsToRxStreamsAdapter(stdin, stdout)
