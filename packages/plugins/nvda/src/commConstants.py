
# Keys and values for the (dictionary) output messages
from enum import Enum


class OutputKeys(Enum):
    SPEECH_VIEWER_STATE = "SPEECH_VIEWER_STATE"
    IS_CONNECTED = "IS_CONNECTED"


class SpeechViewerStates(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


# Settings for the client-server communication
_PORT_FOR_NVDA = 25111  # a11y -> y11a -> 25111, arbitrary otherwise

address = ("localhost", _PORT_FOR_NVDA)
authkey = b'NVDA authentication key'  # for extra confirmation, not security
