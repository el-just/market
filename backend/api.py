import os
import uuid
import shutil
import uuid
import json
import ast

from aiohttp import web
from aiopg.sa import create_engine

from user import User
from market import Market
from product import Product
from label import Label
from offer import Offer
from order import Order
from address import Address
from message import Message

async def handle(request):
    object_name = request.match_info['object']
    method_name = request.match_info['method']

    conn = None
    try: 
        if request.app.get('db_engine') is None:
            db_engine = await create_engine(
                    user='postgres',
                    password=os.environ['MARKET_POSTGRES_PASSWORD'],
                    database=os.environ['MARKET_POSTGRES_DB'],
                    host='postgresql',
                    )
            request.app.db_engine = db_engine

        conn = await request.app.db_engine.acquire()
    except Exception as e:
        pass

    object = globals()[object_name.capitalize()](
            request=request,
            conn=conn,)

    params = {}
    if request.method == 'GET':
        params = parse_params(request.query)
    else:
        if request.headers.get('Content-Type') == 'text/plain;charset=UTF-8' \
                or request.headers.get('content-type') == \
                'text/plain;charset=UTF-8' \
                or request.headers.get('content-type') == 'application/json' \
                or request.headers.get('Content-Type') == 'application/json':
            params = await request.json()
        else:
            post_params = await request.post()
            for key in post_params.keys():
                try:
                    params[key] = json.loads(post_params[key])
                except:
                    try:
                        params[key] = ast.literal_eval(post_params[key])
                    except:
                        params[key] = post_params[key]



    data = await getattr(object, method_name)(**params)
    await getattr(object, 'conn').close()

    def dumps(payload):
        return json.dumps(payload, default=str)

    return web.json_response(data, dumps=dumps) 

def parse_params(raw_params):
    params = {}
    for key in raw_params:
        if len(key.split('-')) > 1:
            path = key.split('-')
            if path[0] not in params.keys():
                params[path[0]] = {}
            params[path[0]][path[1]] = json.loads(raw_params[key])
            if type(params[path[0]][path[1]]) == list and \
                    len(params[path[0]][path[1]]) == 0:
                params[path[0]][path[1]] = None
        else:
            if len(raw_params[key]) == 0:
                params[key] = None
            else:
                params[key] = json.loads(raw_params[key]) if \
                        raw_params[key][0] == '[' else raw_params[key]
                if type(params[key]) == list and len(params[key]) == 0:
                    params[key] = None
    
    return params
