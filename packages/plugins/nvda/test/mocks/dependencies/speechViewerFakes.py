from plugins.nvda.test.mocks.dependencies import wxFake


class _InteractiveFake:
    def __init__(self):
        self._guiFrame = None
        self.isActive = False

    def activate(self):
        self._guiFrame = _GuiFrameFake()
        self.isActive = True

    def destroy(self):
        self._guiFrame.destroy()
        self.isActive = False


def createInteractiveFake():
    return _InteractiveFake()


class _GuiFrameFake:
    def __init__(self):
        self.textCtrl = _TextCtrlFake()

    def destroy(self):
        self.textCtrl.destroy()


class _TextCtrlFake:
    def Bind(self, event, handler):
        if event == wxFake.EVT_WINDOW_DESTROY:
            self.__onDestroy = lambda: handler(event)

    def destroy(self):
        if self.__onDestroy:
            self.__onDestroy()
