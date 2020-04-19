from rx.operators import map, distinct_until_changed

import globalPluginHandler
import wx
import speechViewer

from plugins.nvda.src.commConstants import OutputKeys
from plugins.nvda.src.nvdaMonitor import startMonitoringNvda, SpeechViewerStates
from plugins.nvda.src.outputServer import startOutputServer


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(globalPluginHandler.GlobalPlugin, self).__init__()

        nvdaMonitor = startMonitoringNvda({"speechViewer": speechViewer, "wx": wx})
        outputServer = startOutputServer()

        nvdaMonitor.speechViewerStateStream.pipe(
            map(lambda status: {OutputKeys.SPEECH_VIEWER_STATE: status}),
            distinct_until_changed(),
            map(lambda msgDict: dehydrateMessage(msgDict)),
        ).subscribe(on_next=lambda picklableMsg: outputServer.send(picklableMsg))


def dehydrateMessage(msgDict):
    dehydratedMessageDict = {}

    for enumKey, enumValue in msgDict.items():
        dehydratedMessageDict[enumKey.value] = enumValue.value

    return dehydratedMessageDict


def rehydrateMessage(dehydratedMsgDict):
    hydratedMsgDict = {}

    for key, value in dehydratedMsgDict.items():
        enumKey = OutputKeys(key)
        enumValue = None

        if enumKey is OutputKeys.SPEECH_VIEWER_STATE:
            enumValue = SpeechViewerStates(value)
        else:
            raise NotImplementedError(
                "The new output key hasn't been added to the message hydration method"
            )

        hydratedMsgDict[enumKey] = enumValue

    return hydratedMsgDict
