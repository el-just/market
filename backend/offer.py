from sqlalchemy.sql import text, select, func, literal_column
from aiopg.sa.result import RowProxy
import json

import db
import utils

from link import Link
from product import Product
from market import Market


class Offer:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def exists(self, model):
        offer = model.get("offer") or {}
        entity = model.get("entity") or {}


        offer_id = None
        if offer.get('id') is not None or entity.get('id') is not None:
            query = select([db.offers.c.id]).where(
                        db.offers.c.id == offer.get('id') \
                        if offer.get('id') is not None \
                        else db.offers.c.entity_id == entity.get('id'))

            offer_id = await self.conn.scalar(query)

        return True if offer_id is not None else False

    async def read(self, model):
        offer = model.get("offer") or {}
        entity = model.get("entity") or {}


        model = None
        query = None
        if offer.get('id'):
            query = select([db.offers]).where(
                    db.offers.c.id == offer.get('id'))
        elif entity.get('id'):
            query = select([db.offers]).where(
                    db.offers.c.entity_id == entity.get('id'))

        if query is not None:
            cursor = await self.conn.execute(query)
            offer = await cursor.fetchone()

            cursor = await self.conn.execute(select([db.entities]).where(
                    db.entities.c.id == offer['entity_id']))
            entity = await cursor.fetchone()

            model = {
                "offer":offer,
                "entity":entity,
                }

            if offer["is_node"]:
                model["products"] = await self.read_products(model)
                model["childs"] = await self.read_childs(model)

        return model

    async def create(self, models):
        product_object = Product(conn=self.conn)
        link_object = Link(conn=self.conn)
        link_type = await link_object.offer()

        ids = []
        for model in models:
            offer = model.get("offer") or {}
            entity = model.get("entity") or {}

            entity["object"] = 'offer'
            if 'id' in offer.keys():
                del offer['id']
            if 'entity_id' in offer.keys():
                del offer['entity_id']
            if 'id' in entity.keys():
                del entity['id']

            entity["name"] = model["offer"]["name"]

            entity_id = await self.conn.scalar(
                    db.entities.insert().values(
                        **entity,
                        ).returning(db.entities.c.id))

            offer_id = await self.conn.scalar(db.offers.insert().values(
                        entity_id=entity_id,
                        **offer,
                        ).returning(db.offers.c.id))

            if model.get("products") is not None:
                for product_model in model["products"]:
                    if product_model.get('product', {}).get(
                            'entity_id') is None:
                        existed_model = await product_object.read_or_create(
                                product_model)
                        product_model["product"]["id"] = \
                                existed_model["product"]["id"]
                        product_model["product"]["entity_id"] = \
                                existed_model["product"]["entity_id"]

                await link_object.create([{
                        "object_id": entity_id,
                        "subject_id": product_model["product"]["entity_id"],
                        "type_id": link_type,
                        } for product_model in model["products"]
                    ])

            if model.get("formats"):
                await self.conn.execute(db.offers.update().where(
                        db.offers.c.id == offer_id
                        ).values(is_node=True,))
                for format in model.get("formats"):
                    format["offer"]["parent_id"] = offer_id
                await self.create(model.get("formats"))

            ids.append(offer_id)

        return ids if len(ids) > 0 else None

    async def update(self, models):
        for model in models:
            if model.get("offer") is not None:
                if model.get("entity") is not None:
                    model["entity"]["name"] = model["offer"]["name"]
                await self.conn.execute(db.offers.update().where(
                        db.offers.c.id == model["offer"]['id']
                        ).values(**model["offer"]))

            entity = model.get('entity', {})
            entity["name"] = model["offer"]["name"]
            if model.get('entity') is not None:
                await self.conn.execute(db.entities.update().where(
                        db.entities.c.id == (model["entity"].get('id') \
                            or model["offer"].get('entity_id'))
                        ).values(**model["entity"]))

            if model.get("products") is not None:
                existed_products = await self.read_products(model)
                existed_ids = set([
                        model["product"]["id"] for model in existed_products
                        ]) if existed_products is not None else set()
                new_ids = set([ product_model["product"]["id"] \
                        for product_model in model["products"] ])

                link_object = Link(conn=self.conn)
                link_type = await link_object.offer()
                await link_object.create([{
                        "object_id": model["offer"]["entity_id"],
                        "subject_id": product_model["product"]["entity_id"],
                        "type_id": link_type,
                        } for product_model in model["products"] \
                            if product_model["product"]["id"] in (new_ids -
                                existed_ids)
                    ])
                await link_object.delete([{
                        "object_id": model["offer"]["entity_id"],
                        "subject_id": product_model["product"]["entity_id"],
                        "type_id": link_type,
                        } for product_model in existed_products \
                            if product_model["product"]["id"] in (existed_ids -
                                new_ids)
                    ])

            if model.get("formats") is not None:
                existed_childs = await self.read_childs(model)
                existed_ids = set([
                        model["offer"]["id"] for model in existed_childs
                        ]) if existed_childs is not None else set()
                new_ids = set([ offer_model["offer"]["id"] \
                        for offer_model in model["formats"] \
                        if offer_model["offer"].get("id") is not None ])

                await self.update([ child for child in model["formats"] \
                        if child["offer"].get("id") is not None \
                        and child["offer"]["id"] in (new_ids & existed_ids) ])
                await self.create([ child for child in model["formats"] \
                        if child["offer"].get("id") is None ])
                await self.delete([ child for child in existed_childs \
                        if child["offer"]["id"] in (existed_ids - new_ids) ])

    async def delete(self, models):
        for model in models:
            await self.conn.execute(db.entities.delete().where(
                    db.entities.c.id == model["offer"]["entity_id"]))

    async def update_or_create(self, models):
        ids = []
        for model in models:
            offer_exists = await self.exists(model)

            new_model = None
            if offer_exists:
                await self.update([model])
                ids.append(model["offer"]["id"])
            else:
                offer_ids = await self.create([model])
                ids.append(offer_ids[0])

        return ids

    async def read_products(self, model):
        offer = model.get("offer") or {}
        entity = model.get("entity") or {}

        link_object = Link(conn=self.conn)
        product_object = Product(conn=self.conn)

        product_link_type = await link_object.offer()

        links = await link_object.read({
            "object_id": offer.get('entity_id') or entity.get('id'),
            "type_id": product_link_type,
            })

        products_ids = [links["subject_id"]] if isinstance(links, RowProxy) \
                       else [link["subject_id"] for link in links]
        return await product_object.list(products=products_ids)

    async def read_childs(self, model):
        return await self.list(parent_id=model["offer"]["id"])

    async def list(self, parent_id=None):
        query = select([
                db.offers,
                db.entities.c.name.label('entity_name'),
                db.entities.c.declensions.label('declensions'),
            ]).select_from(db.offers.outerjoin(
                db.entities, 
                db.entities.c.id == db.offers.c.entity_id
            ))

        if parent_id is not None:
            query = query.where(db.offers.c.parent_id == parent_id)

        query = query.group_by(
                db.offers.c.id,
                db.entities.c.name,
                db.entities.c.declensions,
                )
        cursor = await self.conn.execute(query)
        offers = await cursor.fetchall()

        models = []
        for row in offers:
            models.append({
                "offer": { str(key):row[str(key)] \
                           for key in db.offers.c.keys() },
                "entity": {
                    "id":row["entity_id"],
                    "name":row["entity_name"],
                    "declensions":row["declensions"],
                    }
                })

        return models if len(models) > 0 else None


    async def load(self, file):
        offers = json.loads(file.file.read())

        for model in offers:
            if model.get("offer", {}).get("id") is not None:
                del model["offer"]["id"]
            if model.get("offer", {}).get("entity_id") is not None:
                del model["offer"]["entity_id"]
            if model.get("entity", {}).get("id") is not None:
                del model["entity"]["id"]

            if model.get("products") is not None:
                for product in model["products"]:
                    if product.get("product", {}).get("id") is not None:
                        del product["product"]["id"]
                    if product.get("product", {}).get("entity_id") is not None:
                        del product["product"]["entity_id"]

                    if product.get("product", {}).get("is_node") is not None:
                        del product["product"]["is_node"]
                    if product.get("product", {}).get("parent_id") is not None:
                        del product["product"]["parent_id"]
                    if product.get("product", {}).get(
                            "manufacturer_id") is not None:
                        del product["product"]["manufacturer_id"]
                    if product.get("entity", {}).get("id") is not None:
                        del product["entity"]["id"]
                    if product.get("manufacturer", {}).get("id") is not None:
                        del product["manufacturer"]["id"]

                    if product.get("labels") is not None:
                        for label in product.get("labels"):
                            if label.get("label", {}).get("id") is not None:
                                del label["label"]["id"]

            if model.get("formats") is not None:
                for format in model["formats"]:
                    if format.get("offer", {}).get("id") is not None:
                        del format["offer"]["id"]
                    if format.get("offer", {}).get("entity_id") is not None:
                        del format["offer"]["entity_id"]
                    if format.get("offer", {}).get("parent_id") is not None:
                        del format["offer"]["parent_id"]
                    if format.get("entity", {}).get("id") is not None:
                        del format["entity"]["id"]


        await self.create(offers)
