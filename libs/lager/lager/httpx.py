# -*- coding: utf-8 -*-

import asyncio
import atexit

import httpx


SINKS = []


class HttpxSink(object):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.client = httpx.AsyncClient(*args, **kwargs)
        SINKS.append(self)

    async def __call__(self, msg):
        print(msg)
        httpx.post(self.url, data={'msg': msg})

    async def handle(self, message):
        print('async handling', message)
        print(self.url, self.client)
        print(dir(self.client))
        # async with self.client as c:
        #     await c.post(url=self.url, data={'msg': message})
        await self.client.post(url=self.url, data={'msg': message})

    async def await_delete_channels(self):
        await self.client.aclose()

    # @atexit.register
    # def shutdown(self):
    #     print("Shutting down")
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(self.await_delete_channels())


#
# @atexit.register
# def shutdown():
#     print("Shutting down")
#
#
#     async def _shutdown():
#         for sink in SINKS:
#             await sink.client.aclose()
#
#
#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(_shutdown())
#     except RuntimeError:
#         asyncio.run(_shutdown())
