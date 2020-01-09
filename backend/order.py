import db
import utils
from datetime import date, datetime, timedelta

from aiohttp_session import get_session
from aiohttp import web

from sqlalchemy.sql import text, select, func, literal_column, desc
from link import Link
from user import User

from email.mime.text import MIMEText
from email.message import EmailMessage
import aiosmtplib
import telegram
import sms

import utils
from settings import get_config


class Order:
    request = None
    conn = None

    delivery_intervals = [
        'с 12:00 до 15:00',
        'с 15:00 до 18:00',
        'с 18:00 до 21:00',
    ]

    payment_types = [
        'Наличными',
        'Переводом на Сбербанк курьеру',
    ]

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn

    async def create(self, cart, summary):
        min_date = (date.today() + timedelta(days=1)).isoformat()
        if min_date > cart['deliveryDate']:
            return {"error": {"today": date.today().isoformat()}}

        user = User(conn=self.conn)
        user_row = await user.read_or_create(login=cart['personPhone'])

        entity_id = await self.conn.scalar(
                db.entities.insert().values(
                    date_created=datetime.now(),
                    object='order',).returning(db.entities.c.id))

        order_id = await self.conn.scalar(
                db.orders.insert().values(
                    entity_id=entity_id,
                    user_id=user_row['id'],
                    person_name=cart['personName'],
                    person_phone=cart['personPhone'],
                    person_address=cart['personAddress'],
                    person_email=cart['personEmail'] if 'personEmail' in \
                            cart.keys() and cart['personEmail'] is not None \
                            and cart['personEmail'] != '' else None,
                    delivery_date=cart['deliveryDate'],
                    delivery_interval=self.delivery_intervals.index(
                            cart['deliveryInterval']),
                    payment_type=self.payment_types.index(
                            cart['paymentType']),
                    change_from=cart['changeFrom'] if \
                            'changeFrom' in cart.keys() else None,
                    extra_flags=cart['extraFlags'],
                    special_instructions=cart['specialInstructions'] if \
                            'specialInstructions' in cart.keys() else None,
                    status=0,
                    amount=summary['amount'],
                    weight=summary['weight'],
                    ).returning(db.orders.c.id))

        await self.conn.execute(db.entities.update().where(
                db.entities.c.id == entity_id).values(
                    name=order_id))

        link = Link(conn=self.conn)
        link_order = await link.order()
        await link.create([{
                "object_id": entity_id,
                "subject_id": item["offerModel"]["offer"]["entity_id"],
                "type_id": link_order,
                "weight": item["offerModel"]["offer"]["price"],
                "multiplier": item["count"],
                } for item in cart["items"]])

        if len(cart['extraFlags']) > 0 and cart['extraFlags'][0] \
                and 'personEmail' in cart.keys() \
                and cart['personEmail'] is not None \
                and cart['personEmail'] != '':
            #try:
            await self.send_email(
                    utils.Email.order(cart, summary, order_id),
                    "Заказ №%s"%str(order_id),
                    cart['personEmail'],
                    )
            #except Exception as e:
            #    print(e)

        query = await self.conn.execute(
                select([db.orders]).where(
                    (db.orders.c.id == order_id)))
        order = await query.fetchone()

        try:
            await telegram.send('New order: {amount}₽ {weight} кг'.format(
                    amount=summary['amount'], weight=summary['weight'])
            )
        except:
            pass

        await sms.send(cart['personPhone'], (
                'Заказ №{order_id} на сумму {amount}₽ подтверждён\n\n' + \
                'Дата доставки: {delivery_date}\n' + \
                'Интервал: {delivery_interval}\n' + \
                'Оплата: {payment_type}'
                ).format(
                    order_id=str(order["id"]),
                    amount=summary['amount'],
                    delivery_date=(
                        cart['deliveryDate'].split('-')[2],
                        cart['deliveryDate'].split('-')[1],
                        cart['deliveryDate'].split('-')[0],
                        ),
                    delivery_interval=cart['deliveryInterval'].lower(),
                    payment_type=cart['paymentType'].lower(),
                ))

        return {"data": utils.row_to_json(order, db.orders.c.keys())}

    async def cancel(self, order):
        await self.conn.execute(db.entities.delete().where(
            db.entities.c.id == order["entity_id"]))

        if len(order['extra_flags']) > 0 and order['extra_flags'][0] \
                and 'person_email' in order.keys() \
                and order['person_email'] is not None \
                and order['person_email'] != '':
            try:
                await self.send_email(
                        utils.Email.order_cancelled(order),
                        "Отмена заказа №%s"%str(order["id"]),
                        order['person_email'],
                        )
            except Exception as e:
                print(e)

    async def list(self, delivery_date):
        query = '''
            select
                orders.*
                , (
                    select
                        json_agg(y)
                    from (
                        select
                            child_offers.*
                            , entities.declensions
                            , links.weight
                            , links.multiplier
                            , (
                                select
                                    json_agg(x)
                                from (
                                    select
                                        *
                                    from offers parent_offers
                                    where
                                        parent_offers.id = child_offers.parent_id
                                    limit 1
                                ) x
                            ) as parent_offer
                        from links
                            left join offers child_offers on
                                links.subject_id = child_offers.entity_id
                            left join entities on
                                entities.id = child_offers.entity_id
                        where
                            links.object_id = orders.entity_id
                        group by
                            child_offers.id, links.weight
                            ,links.multiplier, entities.declensions
                    ) y
                ) as offers
            from orders
            where orders.delivery_date = '%s'
            order by orders.delivery_date desc, orders.id desc
        '''%delivery_date
        cursor = await self.conn.execute(text(query))
        orders = await cursor.fetchall()

        return [{
                "order": {
                    str(key):order[str(key)] for key in db.orders.c.keys()
                },
                "offers": [{
                    "offer": {
                        str(key):offer[str(key)] for key in db.offers.c.keys()
                    },
                    "entity": {
                        "id":offer["entity_id"],
                        "declensions": offer["declensions"],
                    },
                    "parent_offer": {
                        "offer": {
                            str(key):offer["parent_offer"][0][str(key)] \
                                for key in db.offers.c.keys()
                        }
                    },
                    "price": offer["weight"],
                    "count": offer["multiplier"],
                } for offer in order["offers"]]
            } for order in orders]

    async def summary(self, delivery_date):
        query = '''
            with daily_orders_ids as (
                select
                    orders.entity_id
                from orders
                where orders.delivery_date = '%s'
            )

            select
                child_offers.*
                , entities.declensions
                , sum(order_links.multiplier) as total_count
                , sum(order_links.multiplier) * child_offers.weight as total_weight
                , sum(order_links.multiplier) * child_offers.price as total_price
            from offers child_offers
                left join offers parent_offers on
                    parent_offers.id = child_offers.parent_id
                left join links order_links on
                    child_offers.entity_id = order_links.subject_id
                left join links product_links on
                    parent_offers.entity_id = product_links.object_id
                left join products offer_product on
                    product_links.subject_id = offer_product.entity_id
                left join entities on
                    child_offers.entity_id = entities.id


            where order_links.object_id in (select * from daily_orders_ids)

            group by child_offers.id, offer_product.id, entities.declensions
        '''%delivery_date

        cursor = await self.conn.execute(text(query))
        offers = await cursor.fetchall()

        return [{
                "offer": { str(key):offer[str(key)] \
                          for key in db.offers.c.keys() },
                "entity": {
                    "id": offer["entity_id"],
                    "declensions": offer["declensions"],
                    },
                "count": offer['total_count'],
                "weight": offer['total_weight'],
                "price": offer['total_price'],
                } for offer in offers]


    async def send_email(self, html, subject, email):
        message = EmailMessage()
        message["From"] = os.environ['MARKET_MAIL_SUPPORT']
        message["To"] = '%s, %s'%(email, os.environ['MARKET_MAIL_SALES'])
        message["Subject"] = subject

        message.add_alternative(html, subtype='html')

        await aiosmtplib.send(
                message,
                hostname="smtp.yandex.ru",
                port=465,
                username=os.environ['MARKET_MAIL_SUPPORT'],
                password=os.environ['MARKET_MAIL_SUPPORT_PASSWORD'],
                use_tls=True,
                validate_certs=False,
                )

    async def email_delivery_summary (self, delivery_date):
        config = get_config()
        summary = await self.summary(delivery_date)
        orders = await self.list(delivery_date)

        html = utils.Email.delivery_summary(summary, orders, delivery_date),

        message = EmailMessage()
        message["From"] = os.environ['MARKET_MAIL_SALES']
        message["To"] = os.environ['MARKET_MAIL_ORG']
        message["Subject"] = "Delivery on %s"%str(delivery_date)
        message.add_alternative(html, subtype='html')

        await aiosmtplib.send(
                message,
                hostname="smtp.yandex.ru",
                port=465,
                username=os.environ['MARKET_MAIL_SALES'],
                password=os.environ['MARKET_MAIL_SALES_PASSWORD'],
                use_tls=True,
                validate_certs=False,
                )

    async def save_cart_state(self, cart):
        session = await get_session(self.request)
        session['cart'] = cart
