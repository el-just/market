import db

from sqlalchemy.sql import text, select, func

class Manufacturer:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def read(self, model):
        manufacturer = None
        if model.get("id") is not None:
            query = select([db.manufacturers]).where(
                        db.manufacturers.c.id == model["id" ])

            cursor = await self.conn.execute(query)
            manufacturer = await cursor.fetchone()
        elif model.get("name") is not None:
            query = select([db.manufacturers]).where(
                        db.manufacturers.c.name == model["name"])
            cursor = await self.conn.execute(query)
            manufacturer = await cursor.fetchone()

        return manufacturer

    async def read_or_create(self, model):
        new_model = await self.read(model)

        if new_model is None:
            manufacturer_ids = await self.create([model])
            new_model = await self.read({"id":manufacturer_ids[0]})

        return new_model


    async def create(self, models):
        ids = []
        for model in models:
            if 'id' in model.keys():
                del model['id']
            if 'entity_id' in model.keys():
                del model['entity_id']

            if model.get('country_id') is None:
                entity_id = await self.conn.scalar(
                        db.entities.insert().values(
                            name=model["name"],
                            object='country',).returning(
                                db.entities.c.id))
                model["country_id"] = await self.conn.scalar(
                        db.countries.insert().values(
                            entity_id=entity_id,
                            name=model["name"],
                            ).returning(
                                db.countries.c.id))

            entity_id = await self.conn.scalar(
                    db.entities.insert().values(
                        name=model["name"],
                        ).returning(
                            db.entities.c.id))
            manufacturer_id = await self.conn.scalar(
                    db.manufacturers.insert().values(
                        **model,
                        entity_id=entity_id,
                        ).returning(
                            db.manufacturers.c.id))

            ids.append(manufacturer_id)

        return ids
