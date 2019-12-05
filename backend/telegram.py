import urllib.parse
import aiohttp
import os

chat_id = 276455649
key = os.environ['MARKET_TELEGRAM_KEY']
base_path = 'https://api.telegram.org/bot%s/'%key

async def send(message):
    params = {'chat_id': chat_id, 'text': message}
    request = (base_path+'sendMessage?'+urllib.parse.urlencode(params))
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(request) as resp:
            text = await resp.text()
