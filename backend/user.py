import sqlalchemy as sa
from sqlalchemy.sql import text, select

from passlib.hash import sha256_crypt
from datetime import date
import random
import string
import json

from aiohttp import web
from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)
from aiohttp_session import get_session

import db
from db_auth import check_credentials
from settings import config


class User:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def read_or_create(self, login=None):
        user_id = await self.conn.scalar(select([db.users.c.id]).where(
                db.users.c.login == login))

        if user_id is None:
            password = self.random_string()
            entity_id = await self.conn.scalar(db.entities.insert().values(
                    name=login,
                    date_created=date.today(),
                    object='user',).returning(db.entities.c.id))
            user_id = await self.conn.scalar(db.users.insert().values(
                login=login,
                passwd=sha256_crypt.hash(
                    password + config['auth']['extra']),
                entity_id=entity_id,).returning(db.users.c.id))

        cursor = await self.conn.execute(select([db.users]).where(
                db.users.c.id == user_id))
        return await cursor.fetchone()

    async def login(self, login, password):
        response = web.HTTPFound('/')
        if await check_credentials(self.request.app.db_engine, login, password):
            await remember(self.request, response, login)
            return {"success": True}

        return {"success": False}

    async def logout(self):
        response = web.HTTPFound('/')
        await forget(self.request, response)

    async def info(self):
        response = {'data':{'auth': True}}

        try:
            await check_authorized(self.request)
        except Exception as e:
            response['data']['auth'] = False

        session = await get_session(self.request)
        if 'cart' in session.keys():
            response['data']['cart'] = session['cart']

        return response

    async def is_superuser(self):
        try:
            login = await check_authorized(self.request)
            is_superuser = await self.conn.scalar(
                    select([db.users.c.is_superuser]).where(
                        db.users.c.login == login))
            return {"data":{"is_superuser": is_superuser}}
        except Exception as e:
            return {"data":{"is_superuser": False}}

    def random_string(self, string_length=7):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(string_length))
