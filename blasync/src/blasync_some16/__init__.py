from .async_loop import AsyncModalOperatorMixin,  ensure_async_loop, setup_asyncio_executor

import asyncio

def run_async_blocking(act):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(act())

def run_async(act, callback=None):
    async_task = asyncio.ensure_future(act())
    if callback is not None:
        async_task.add_done_callback(callback)
    ensure_async_loop()
    return {'FINISHED'}