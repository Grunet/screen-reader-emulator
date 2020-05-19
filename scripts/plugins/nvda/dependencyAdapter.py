# Dependency handling based on https://nvda-addons.groups.io/g/nvda-addons/topic/how_to_import_an_external/25136329?p=,,,20,0,0,0::recentpostdate%2Fsticky,,,20,2,0,25136329 # noqa

import sys
import os

# Not deleting these after the plugin import in case of runtime imports later
# In case of duplicates NVDA core should use modules from earlier in the sys.path list

sys.path.append(os.path.join(os.path.dirname(__file__), partialPathToAppDependencies))

from . import filenameOfEntryPoint

GlobalPlugin = filenameOfEntryPoint.GlobalPlugin
