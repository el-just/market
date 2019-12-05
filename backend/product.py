import db

from sqlalchemy.sql import text, select, func
from aiopg.sa.result import RowProxy

from label import Label
from link import Link
from manufacturer import Manufacturer
import yc


class Product:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def exists(self, model):
        product = model.get('product') or {}
        entity = model.get('entity') or {}

        product_id = None
        if product.get("id") is not None or entity.get('id') is not None:
            query = select([db.products.c.id]).where(
                        db.products.c.id == product.get('id') \
                        if product.get('id') is not None \
                        else db.product.c.entity_id == entity.get('id'))

            product_id = await self.conn.scalar(query)

        return True if product_id is not None else False

    async def read(self, model):
        product = model.get('product') or {}
        entity = model.get('entity') or {}



        if product.get('id'):
            query = select([db.products]).where(
                    db.products.c.id == product.get('id'))
        elif entity.get('id'):
            query = select([db.products]).where(
                    db.products.c.entity_id == entity.get('id'))
        else:
            query = select([db.products]).select_from(db.products.outerjoin(
                    db.manufacturers,
                    db.manufacturers.c.id == db.products.c.manufacturer_id
                )).where(
                    (db.products.c.name == product.get('name')) & \
                    (db.manufacturers.c.name == \
                        model["manufacturer"]["name"]))

        cursor = await self.conn.execute(query)
        product = await cursor.fetchone()

        if product is None:
            return None

        cursor = await self.conn.execute(select([db.entities]).where(
                db.entities.c.id == product['entity_id']))
        entity = await cursor.fetchone()

        cursor = await self.conn.execute(select([db.manufacturers]).where(
                db.manufacturers.c.id == product['manufacturer_id']))
        manufacturer = await cursor.fetchone()

        return {
                "product":product,
                "entity":entity,
                "manufacturer":manufacturer, 
                }

    async def create(self, models):
        label_object = Label(conn=self.conn)
        label_type = await label_object.cooking_class()
        link_object = Link(conn=self.conn)
        link_type = await link_object.label()

        manufacturer_object = Manufacturer(conn=self.conn)
        ids = []
        for model in models:
            product = model.get('product') or {}
            entity = model.get('entity') or {}

            entity["object"] = 'product'
            if 'id' in product.keys():
                del product['id']
            if 'entity_id' in product.keys():
                del product['entity_id']
            if 'id' in entity.keys():
                del entity['id']

            entity["name"] = model["product"]["name"]

            if model.get('manufacturer') is not None \
                    and model["product"].get("manufacturer_id") is None:
                manufacturer = await manufacturer_object.read_or_create(
                        model.get('manufacturer'))
                model["product"]["manufacturer_id"] = \
                        manufacturer["id"]

            entity["name"] = product["name"]

            entity_id = await self.conn.scalar(
                    db.entities.insert().values(
                        **entity,
                        ).returning(db.entities.c.id))
            product_id = await self.conn.scalar(
                    db.products.insert().values(
                        entity_id=entity_id,
                        **product,
                        ).returning(db.products.c.id))

            if model.get('labels') is not None:
                for label_model in model["labels"]:
                    label_model["label"]["type_id"] = label_type
                    label = await label_object.read_or_create(label_model)
                    label_model["entity"] = label["entity"]

                await link_object.create([{
                        'object_id': entity_id,
                        'subject_id': label["entity"]["id"],
                        'type_id': link_type,
                    } for label in model["labels"]])

            ids.append(product_id)

        return ids

    async def update(self, models):
        for model in models:
            entity = model.get('entity', {})
            entity["name"] = model["product"]["name"]

            if model.get('manufacturer') is not None \
                    and model["product"].get("manufacturer_id") is None:
                manufacturer_object = Manufacturer(conn=self.conn)
                manufacturer = await manufacturer_object.read_or_create(
                        model.get('manufacturer'))
                model["product"]["manufacturer_id"] = \
                        manufacturer["id"]

            if model.get('product') is not None:
                await self.conn.execute(db.products.update().where(
                        db.products.c.id == model["product"]['id']).values(
                            **model.get('product')))

            if entity is not None:
                await self.conn.execute(db.entities.update().where(
                        db.entities.c.id == (entity.get('id') \
                            or model["product"].get('entity_id'))
                        ).values(**entity))

            if model.get('labels') is not None:
                label = Label(conn=self.conn)
                link = Link(conn=self.conn)
                link_type = await link.label()

                links_all = await link.read({
                        'object_id':model['product']['entity_id'],
                        })

                if isinstance(links_all, RowProxy):
                    links_all=[links_all]

                existed_links = set([link['subject_id'] for link in links_all] \
                        if links_all is not None else [])
                new_links = set([
                        label["label"]["entity_id"] \
                            for label in model["labels"]])

                links_to_add = new_links - existed_links
                links_to_remove = existed_links - new_links

                for label_id in links_to_add:
                    await link.read_or_create({
                            'object_id': model['product']['entity_id'],
                            'subject_id': label_id,
                            'type_id': link_type,
                            })

                await link.delete([{
                        "object_id": model['product']['entity_id'],
                        "subject_id":label_id,
                        "type_id":link_type,
                        } for label_id in links_to_remove])

    async def delete(self, models):
        for model in models:
            await self.conn.execute(db.entities.delete().where(
                    db.entities.c.id == model["product"]["entity_id"]))

    async def read_or_create(self, model):
        new_model = await self.read(model)

        if new_model is None:
            products = await self.create([model])
            new_model = await self.read({"product":{"id":products[0]}})

        return new_model

    async def update_or_create(self, models, file=None):
        ids = []
        for model in models:
            product = model.get('product') or {}
            entity = model.get('entity') or {}

            if file is not None:
                file_path = yc.save_file(file)
                product['img'] = file_path

            product_exists = await self.exists(model)
            if product_exists:
                await self.update([model])
                ids.append(product.get('id'))
            else:
                product_id = await self.create([model])
                ids.append(product_id)


        return ids

    async def list(self, products=None):
        query = select([
                db.products,
                db.entities.c.name.label('entity_name'),
                db.entities.c.declensions.label('declensions'),
                db.manufacturers.c.name.label('manufacturer_name'),
                func.array_agg(
                    text('ARRAY[labels.name, labels.entity_id::varchar]')
                    ).label('labels')
                ],
            ).select_from(db.products.outerjoin(db.links, 
                    db.links.c.object_id == db.products.c.entity_id
                    ).outerjoin(
                        db.entities,
                        db.entities.c.id == db.products.c.entity_id
                ).outerjoin(
                    db.manufacturers,
                    db.manufacturers.c.id == db.products.c.manufacturer_id
                ).outerjoin(
                    db.labels,
                    db.labels.c.entity_id == db.links.c.subject_id)

            )

        print(query.compile())

        if products is not None:
            query = query.where(db.products.c.entity_id.in_(products))

        query = query.group_by(db.products.c.id, db.entities.c.name,
                        db.entities.c.declensions, db.manufacturers.c.name
                        ).order_by(db.entities.c.name)

        query = await self.conn.execute(query)
        products = await query.fetchall()

        models = []
        for row in products:
            models.append({
                "product": { str(key):row[str(key)] \
                           for key in db.products.c.keys() },
                "entity": {
                    "id":row["entity_id"],
                    "name":row["entity_name"],
                    "declensions":row["declensions"],
                    },
                "manufacturer": {
                    "id": row["manufacturer_id"],
                    "name": row["manufacturer_name"],
                    },
                "labels": [{
                    "label": {
                        "name": label_model[0],
                        "entity_id": int(label_model[1]),
                        },
                    "entity": {
                        "id": int(label_model[1]),
                        }
                    } for label_model in row["labels"] \
                            if label_model is not None \
                            and label_model[1] is not None],
                })

        return models if len(models) > 0 else None
