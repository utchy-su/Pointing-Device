import asyncio


async def sample(num):
    await asyncio.sleep(3)
    print(num)


async def check_async():
    for i in range(10):
        await sample(i)

    return True


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(check_async())
    asyncio.ensure_future(check_async())
    loop.run_forever()