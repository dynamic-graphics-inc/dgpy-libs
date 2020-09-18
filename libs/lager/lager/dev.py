# -*- coding: utf-8 -*-

import httpx


SINKS = []


class HttpxSink(object):


    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.client = httpx.AsyncClient(*args, **kwargs)
        SINKS.append(self)


    async def __call__(self, msg):
        httpx.post(self.url, data={
            'msg': msg
            })


    async def handle(self, message):
        await self.client.post(url=self.url, data={
            'msg': message
            })


    async def await_delete_channels(self):
        await self.client.aclose()
