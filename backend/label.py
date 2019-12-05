import db
import utils
from sqlalchemy.sql import  select

class Label:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn

    async def read(self, model):
        label = model.get('label', {})
        entity = model.get('entity', {})


        if label.get('id'):
            query = select([db.labels]).where(
                    db.labels.c.id == label.get('id'))
        elif entity.get('id'):
            query = select([db.labels]).where(
                    db.labels.c.entity_id == entity.get('id'))
        else:
            if label.get('type_id') is None:
                label['type_id'] = await self.cooking_class()
            query = select([db.labels]).where(
                    (db.labels.c.name == label.get('name')) & \
                    (db.labels.c.type_id == label.get('type_id')))

        cursor = await self.conn.execute(query)
        label = await cursor.fetchone()

        if label is None:
            return None

        cursor = await self.conn.execute(select([db.entities]).where(
                db.entities.c.id == label['entity_id']))
        entity = await cursor.fetchone()

        return {"label":label,
                "entity":entity,}

    async def create(self, models):
        ids = []
        for model in models:
            label = model.get('label', {})
            entity = model.get('entity', {})

            entity["name"] = label["name"]
            entity["object"] = 'label'
            if 'id' in label.keys():
                del label['id']
            if 'entity_id' in label.keys():
                del label['entity_id']
            if 'id' in entity.keys():
                del entity['id']

            if label.get('type_id') is None:
                label['type_id'] = await self.cooking_class()

            entity_id = await self.conn.scalar(
                    db.entities.insert().values(
                        **entity,
                        ).returning(db.entities.c.id))
            label_id = await self.conn.scalar(
                    db.labels.insert().values(
                        entity_id=entity_id,
                        **label,
                        ).returning(db.labels.c.id))

            ids.append(label_id)

        return ids

    async def read_or_create(self, model):
        new_model = await self.read(model)

        if new_model is None:
            label_ids = await self.create([model])
            new_model = await self.read({'label':{'id':label_ids[0]}})

        return new_model

    async def cooking_class(self):
        label_type = await self.conn.scalar(select([db.label_types.c.id]).where(
                db.label_types.c.name == 'cooking_class'))

        if label_type is None:
            label_type = await self.conn.scalar(db.label_types.insert().values(
                   name="cooking_class",
                   description="Cooking classification of products",).returning(
                       db.label_types.c.id))

        return label_type

    async def list(self):
        query = select([db.labels]).where(
                db.labels.c.type_id == await self.cooking_class())
        columns = query.columns
        cursor = await self.conn.execute(query)
        labels = await cursor.fetchall()

        return [{
                "label": {
                    "id": label["id"],
                    "entity_id": label["entity_id"],
                    "name": label["name"]},
                } for label in labels]
