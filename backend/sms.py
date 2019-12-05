import urllib.parse
import base64
import os
import aiohttp

__host = 'gate.prostor-sms.ru'
__url = 'http://api.prostor-sms.ru/messages/v2/send/?'
__market_name = 'Veggies'
__login = os.environ['MARKET_SMS_LOGIN']
__password = os.environ['MARKET_SMS_PASSWORD']


async def send(phone, text,
        statusQueueName=None, scheduleTime=None, wapurl = None):
    basic_auth = str(base64.b64encode(
            ('%s:%s'%(__login, __password)).encode("utf-8")), 'utf-8')
    params = {
        'phone': '+%s'%phone,
        'text': text,
        'sender': __market_name,
        #'statusQueueName': statusQueueName,
        #'scheduleTime': scheduleTime,
        #'wapurl': wapurl
    }
    headers = {"Authorization": "Basic %s"%(basic_auth)}

    '''
    request = __url + urllib.parse.urlencode(params)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(request) as resp:
            text = await resp.text()
            print(text)
    '''
