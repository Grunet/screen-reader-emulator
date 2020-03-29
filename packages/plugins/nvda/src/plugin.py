import globalPluginHandler

from scriptHandler import script
import ui


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(globalPluginHandler.GlobalPlugin, self).__init__()

    @script(gesture="kb:NVDA+shift+v")
    def script_announceNVDAVersion(self, gesture):
        ui.message("Is this working?")
