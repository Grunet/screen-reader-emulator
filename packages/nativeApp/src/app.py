import sys
import asyncio

from nativeApp.src.adapters.extensionClientAdapter import createConnectionToExtension

from nativeApp.src.adapters.nvdaClientAdapter import createConnectionToNVDA


async def main():
    extensionConnection = createConnectionToExtension(sys.stdin, sys.stdout)

    extensionConnection.inputStream.on_next("This is from the native app")
    extensionConnection.outputStream.subscribe(
        on_next=lambda msg: extensionConnection.inputStream.on_next(msg)
    )

    # If/when a user can pick a screen reader to use, this should be done conditionally
    nvdaConnection = createConnectionToNVDA()
    nvdaConnection.outputStream.subscribe(
        on_next=lambda msg: extensionConnection.inputStream.on_next(msg)
    )

    await __waitForOutstandingTasksToFinish()


async def __waitForOutstandingTasksToFinish():
    while True:
        pending = asyncio.all_tasks()
        pending.remove(asyncio.current_task())  # Removes the main() coroutine

        if not pending:
            break

        await asyncio.gather(*pending)


asyncio.run(main())
