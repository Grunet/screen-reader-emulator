import sys
import os

# Not deleting these after the plugin import in case of dynamic imports later
sys.path.append(os.path.join(os.path.dirname(__file__), partialPathToAppDependencies))

from . import filenameOfEntryPoint

GlobalPlugin = filenameOfEntryPoint.GlobalPlugin
