# To hit breakpoints set in VS Code later on
# breakpoint()  # 0) Uncomment this
# 1) Run the harness from the tasks.json task
# 2) Use the Python launch.json debug config to attach to this process
# 3) Then type the keyword "continue" at the PDB prompt

import plugins.nvda.test.harness.staticMocks  # for side-effects only  # noqa

# Use the properties on this object to simulate various kinds of input
from plugins.nvda.test.harness.interactiveMocks import Fakes  # noqa

from threading import Thread


# Running the plugin in a separate thread to allow for interactive input
def __runPlugin():
    from plugins.nvda.src.plugin import GlobalPlugin

    GlobalPlugin()


t = Thread(target=__runPlugin)
t.daemon = True
t.start()
