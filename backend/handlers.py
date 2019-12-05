from textwrap import dedent

import aiohttp
from aiohttp import web
from aiofile import AIOFile

from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)
from aiohttp_session import get_session

from db_auth import check_credentials
from settings import get_config
import api


class Web(object):
    async def api(self, request):
        return await api.handle(request)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')

        return ws

    def configure(self, app):
        router = app.router
        router.add_route('GET', '/api/{object}/{method}', self.api, name='api')
        router.add_route('POST', '/api/{object}/{method}', self.api, name='api')
        app.add_routes([web.get('/ws', self.websocket_handler)])
