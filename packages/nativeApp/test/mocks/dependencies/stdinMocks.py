import sys
import json
import struct


def mockStdinBuffer():
    from io import BytesIO

    sys.stdin = lambda: None
    setattr(sys.stdin, "buffer", BytesIO())


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
