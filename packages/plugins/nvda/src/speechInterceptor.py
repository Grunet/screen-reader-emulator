import globalPluginHandler

from scriptHandler import script
import ui


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @script(gesture="kb:NVDA+shift+v")
    def script_announceNVDAVersion(self, gesture):
        ui.message("Is this working?")

