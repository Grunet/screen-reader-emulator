import sys
import asyncio

from nativeApp.src.adapters.extensionClientAdapter import createConnectionToExtension


async def main():
    extensionConnection = createConnectionToExtension(sys.stdin, sys.stdout)

    extensionConnection.inputStream.on_next("This is from the native app")
    extensionConnection.outputStream.subscribe(on_next=lambda msg: print(msg))

    await __waitForOutstandingTasksToFinish()


async def __waitForOutstandingTasksToFinish():
    while True:
        pending = asyncio.all_tasks()
        pending.remove(asyncio.current_task())  # Removes the main() coroutine

        if not pending:
            break

        await asyncio.gather(*pending)


asyncio.run(main())
