import sys
import os
import asyncio
from passlib.hash import sha256_crypt
from datetime import date, datetime, timedelta

from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.sql import text, select, func, literal_column, desc

import db
from settings import config

class DB_init:
    conn = None

    def __init__(self, conn):
        self.conn = conn


    async def register_super(self, login=None, password=None):
        if login is not None and password is not None:
            entity_id = await self.conn.scalar(
                    select([db.users.c.entity_id]).where(
                        db.users.c.is_superuser == True))

            if entity_id is None:
                entity_id = await self.conn.scalar(db.entities.insert().values(
                    name=login,
                    date_created=datetime.now(),
                    object='user',).returning(db.entities.c.id))
                await self.conn.execute(db.users.insert().values(
                        login=login,
                        passwd=sha256_crypt.hash(
                            password + config['auth']['extra']),
                        is_superuser=True,
                        entity_id=entity_id,))

    async def generate_orders(self):
        last_order_id = await self.conn.scalar(
                select([db.orders.c.id]).order_by(desc(db.orders.c.id)))

        if last_order_id is None or last_order_id < 1244:
            for idx in range(0, 1244):
                entity_id = await self.conn.scalar(
                        db.entities.insert().values(
                            date_created=date.today()-timedelta(days=1),
                            object='order',).returning(db.entities.c.id))
                order_id = await self.conn.scalar(
                        db.orders.insert().values(
                            entity_id=entity_id,
                            user_id=1,
                            person_name='personName',
                            person_phone='personPhone',
                            person_address='personAddress',
                            person_email='personEmail',
                            delivery_date=date.today()-timedelta(days=1),
                            delivery_interval=0,
                            payment_type=0,
                            status=0,
                            amount=0,
                            weight=0,
                            ).returning(db.orders.c.id))

    async def settings(self)
        await self.conn.scalar(
                db.settings.insert().values(
                    name="stage",
                    value="testing",
                    ).returning(db.settings.c.id))

async def go(args):
    async with create_engine(
            user='postgres',
            password=os.environ['MARKET_POSTGRES_PASSWORD'],
            database=os.environ['MARKET_POSTGRES_DB'],
            host='postgresql',
            ) as engine:

        async with engine.acquire() as conn:
            db_init = DB_init(conn=conn)
            await db_init.register_super(
                    login=args[0] if len(args) > 1 else None,
                    password=args[1] if len(args) > 1 else None,
                    )
            await db_init.generate_orders()
            await db_init.settings()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(sys.argv[1:]))

