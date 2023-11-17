# Test the Task.exception() method

try:
    import asyncio
except ImportError:
    print("SKIP")
    raise SystemExit


async def task(t, exc=None):
    if t >= 0:
        await asyncio.sleep(t)
    if exc:
        raise exc


async def main():
    # Task that is not done yet raises an InvalidStateError
    print("=" * 10)
    t = asyncio.create_task(task(1))
    await asyncio.sleep(0)
    try:
        t.exception()
        assert False, "Should not get here"
    except Exception as e:
        print("Tasks that aren't done yet raise an InvalidStateError:", repr(e))

    # Task that is cancelled raises CancelledError
    print("=" * 10)
    t = asyncio.create_task(task(1))
    t.cancel()
    await asyncio.sleep(0)
    try:
        print(repr(t.exception()))
        print(t.cancelled())
        assert False, "Should not get here"
    except asyncio.CancelledError as e:
        print("Cancelled tasks cannot retrieve exception:", repr(e))

    # Task that starts, runs and finishes without an exception should return None
    print("=" * 10)
    t = asyncio.create_task(task(0.01))
    await t
    print("None when no exception:", t.exception())

    # Task that raises immediately should return that exception
    print("=" * 10)
    t = asyncio.create_task(task(-1, ValueError))
    try:
        await t
        assert False, "Should not get here"
    except ValueError as e:
        pass
    print("Returned Exception:", repr(t.exception()))

    # Task returns `none` when somehow an exception isn't in data
    print("=" * 10)
    t = asyncio.create_task(task(-1))
    await t
    t.data = "Example"
    print(t.exception())


asyncio.run(main())
