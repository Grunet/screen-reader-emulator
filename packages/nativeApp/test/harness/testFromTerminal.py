# To hit breakpoints set in VS Code later on
# breakpoint()  # 0) Uncomment this
# 1) Run the harness from the tasks.json task
# 2) Use the Python launch.json debug config to attach to this process
# 3) Then type the keyword "continue" at the PDB prompt

# Use the properties on this object to simulate various kinds of input
from nativeApp.test.harness.interactiveMocks import Fakes  # noqa

from threading import Thread


# Running the nativeApp in a separate thread to allow for interactive input
def __runApp():
    import runpy

    runpy.run_module("nativeApp.src.app")


t = Thread(target=__runApp)
t.daemon = True
t.start()
