# To hit breakpoints set in VS Code later on
# breakpoint()  # 0) Uncomment this
# 1) Run the harness from the tasks.json task
# 2) Use the Python launch.json debug config to attach to this process
# 3) Then type the keyword "continue" at the PDB prompt

import sys
import json
import struct

from threading import Thread


# Use this to simulate providing input to the nativeApp
def sendMessageToStdin(message):
    __writeToStdinBuffer(__encodeMessage(message))


def __writeToStdinBuffer(encodedMessage):
    posBeforeWrite = sys.stdin.buffer.tell()

    sys.stdin.buffer.write(encodedMessage["length"])
    sys.stdin.buffer.write(encodedMessage["content"])
    sys.stdin.buffer.flush()

    sys.stdin.buffer.seek(posBeforeWrite)


def __encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent).encode("utf-8")
    encodedLength = struct.pack("@I", len(encodedContent))

    return {"length": encodedLength, "content": encodedContent}


# Mocks
def __overwriteStdinWithMock():
    from io import BytesIO

    sys.stdin = lambda: None
    setattr(sys.stdin, "buffer", BytesIO())


# Running the nativeApp in a separate thread to allow for interactive input
def __runApp():
    __overwriteStdinWithMock()

    import runpy

    runpy.run_module("nativeApp.src.app")


t = Thread(target=__runApp)
t.daemon = True
t.start()
