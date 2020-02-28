import sys
import asyncio

from extension.background.src.clients.nativeClient import connectToExtension


async def main():
    a = connectToExtension(sys.stdin, sys.stdout)

    a.inputStream.on_next("This is from the native app")
    a.outputStream.subscribe(on_next=lambda msg: print(msg))

    await __waitForOutstandingTasksToFinish()


async def __waitForOutstandingTasksToFinish():
    while True:
        pending = asyncio.all_tasks()
        pending.remove(asyncio.current_task())  # Removes the main() coroutine

        if not pending:
            break

        await asyncio.gather(*pending)


asyncio.run(main())
