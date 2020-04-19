from plugins.nvda.test.mocks.dependencies import wxFake, globalPluginHandlerFake

import sys

sys.modules["wx"] = wxFake
sys.modules["globalPluginHandler"] = globalPluginHandlerFake
