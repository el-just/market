import sqlalchemy as sa

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

import db
from settings import config


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, dbengine):
        self.dbengine = dbengine

    async def authorized_userid(self, identity):
        async with self.dbengine.acquire() as conn:
            query = db.users.count().where(db.users.c.login == identity)
            ret = await conn.scalar(query)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False

        async with self.dbengine.acquire() as conn:
            query = db.users.select().where(db.users.c.login == identity)
            ret = await conn.execute(query)
            user = await ret.fetchone()
            if user is not None:
                user_id = user[0]
                is_superuser = user[3]
                if is_superuser:
                    return True

                where = db.permissions.c.user_id == user_id
                query = db.permissions.select().where(where)
                ret = await conn.execute(query)
                result = await ret.fetchall()
                if ret is not None:
                    for record in result:
                        if record.perm_name == permission:
                            return True

            return False


async def check_credentials(db_engine, username, password):
    async with db_engine.acquire() as conn:
        query = db.users.select().where(db.users.c.login == username)
        ret = await conn.execute(query)
        user = await ret.fetchone()
        if user is not None:
            hash = user[2]
            return sha256_crypt.verify(password + config['auth']['extra'], hash)
    return False
