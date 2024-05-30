import time
import asyncio


def synchronous_database_query():
    start_time = time.time()
    time.sleep(2)
    end_time = time.time()
    return end_time - start_time


async def asynchronous_database_query():
    await asyncio.sleep(2)


async def main():
    # Synchronous usage
    time_sync = synchronous_database_query()
    print("Synchronous query execution time:", time_sync, "seconds")

    # Asynchronous usage
    asynchronous_database_query()
    # print("Asynchronous query execution time:", "seconds")
    print("Your email has been sent")


# Run the event loop to execute the asynchronous code
asyncio.run(main())
