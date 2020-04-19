from threading import Timer

from rx.subject import Subject

from plugins.nvda.src.commConstants import SpeechViewerStates


class _NvdaMonitor:
    def __init__(self, nvdaModules):
        self.__speechViewerMonitor = _SpeechViewerMonitor(nvdaModules)

    @property
    def speechViewerStateStream(self):
        return self.__speechViewerMonitor.stateStream


class _SpeechViewerMonitor:
    def __init__(self, nvdaModules):
        self.__nvdaModules = nvdaModules

        self.__stateStream = Subject()  # Could this be an Observable instead?

        self.__startMonitoring()

    @property
    def stateStream(self):
        return self.__stateStream

    def __startMonitoring(self, delay=0):
        thread = Timer(delay, self.__waitForActivation)
        thread.daemon = True
        thread.start()

    def __waitForActivation(self):
        while True:
            if (not self.__nvdaModules["speechViewer"]._guiFrame) or (
                not self.__nvdaModules["speechViewer"].isActive
            ):
                self.__stateStream.on_next(SpeechViewerStates.INACTIVE)
            else:
                self.__nvdaModules["speechViewer"]._guiFrame.textCtrl.Bind(
                    self.__nvdaModules["wx"].EVT_TEXT, self.__monitorTextChangeHandler,
                )

                self.__nvdaModules["speechViewer"]._guiFrame.textCtrl.Bind(
                    self.__nvdaModules["wx"].EVT_WINDOW_DESTROY,
                    self.__monitorDestroyHandler,
                )

                self.__stateStream.on_next(SpeechViewerStates.ACTIVE)
                break

    def __monitorTextChangeHandler(self, event):
        pass

    def __monitorDestroyHandler(self, event):
        self.__stateStream.on_next(SpeechViewerStates.INACTIVE)

        # The isActive flag is still True here in NVDA's speechViewer.py implementation
        # So this is trying to delay until it finishes being set back to False
        self.__startMonitoring(1)  # In case the speech viewer is reopened


def startMonitoringNvda(nvdaModules):
    return _NvdaMonitor(nvdaModules)
