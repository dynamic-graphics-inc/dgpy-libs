from lager.httpx import HttpxSink
from lager import LAGER_PORT
from lager import LOG as log
import httpx


httpx.post('http://localhost:52437/', data={
    'herm': 234
    })

async def herm(message):
    httpx.post('http://localhost:52437/', data={
        'msg': message
        })

httpsink = HttpxSink(url=f'http://localhost:{LAGER_PORT}/')
log.add(
    httpsink.handle,
    # level="DEBUG",
    serialize=True
    )

async def main():
    log.info('something else')
    log.debug('something else')
    # log.info('some other thing herm', howdy="something")
    log.warning('some warning')
    # log = pour_lager(filepath='herm.log')
    log.info('howdy')
    # await log.complete()

import asyncio as aio


aio.run(main())
