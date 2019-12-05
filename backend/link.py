from sqlalchemy.sql import text, select
import db

class Link:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def read(self, link=None):
        link = link or {}
        if link.get('id') is not None:
            query = select([db.links]).where(
                    db.links.c.id == link.get('id'))
        elif link.get('object_id') is not None \
                and link.get('subject_id') is not None:
            query = select([db.links]).where(
                        (db.links.c.object_id == link['object_id']) & \
                        (db.links.c.subject_id == link['subject_id']) & \
                        (db.links.c.type_id == link['type_id']))
        elif link.get('object_id') is not None \
                and link.get('type_id') is not None:
            query = select([db.links]).where(
                        (db.links.c.object_id == link['object_id']) & \
                        (db.links.c.type_id == link['type_id']))
        elif link.get('subject_id') is not None \
                and link.get('type_id') is not None:
            query = select([db.links]).where(
                        (db.links.c.subject_id == link['subject_id']) & \
                        (db.links.c.type_id == link['type_id']))
        elif link.get('object_id') is not None:
            query = select([db.links]).where(
                    db.links.c.object_id == link.get('object_id'))

        links = None
        if query is not None:
            cursor = await self.conn.execute(query)
            links = await cursor.fetchall()

        if len(links) == 0:
            return None

        return links[0] if len(links) == 1 else links

    async def create(self, links=None):
        ids = []
        for link in links:
            link_id = await self.conn.scalar(db.links.insert().values(
                    **link
                    ).returning(db.links.c.id))
            ids.append(link_id)

        return ids
        
    async def delete(self, links):
        for link in links:
            await self.conn.execute(db.links.delete().where(
                    (db.links.c.object_id == link["object_id"]) & \
                    (db.links.c.subject_id == link["subject_id"]) & \
                    (db.links.c.type_id == link["type_id"])))


    async def read_or_create(self, link):
        model = await self.read(link)

        if model is None:
            link_ids = await self.create([link])
            model = await self.read({'id': link_ids[0]})

        return model



    async def label(self):
        link_type = await self.conn.scalar(select([db.link_types.c.id]).where(
                db.link_types.c.name == 'label'))

        if link_type is None:
            link_type = await self.conn.scalar(db.link_types.insert().values(
                   name="label",
                   description="Links with labels",).returning(
                       db.link_types.c.id))

        return link_type

    async def offer(self):
        link_type = await self.conn.scalar(select([db.link_types.c.id]).where(
                db.link_types.c.name == 'offer').as_scalar())

        if link_type is None:
            link_type = await self.conn.scalar(db.link_types.insert().values(
                   name="offer",
                   description="Links of offers with products",).returning(
                       db.link_types.c.id))


        return link_type

    async def order(self):
        link_type = await self.conn.scalar(select([db.link_types.c.id]).where(
                db.link_types.c.name == 'order').as_scalar())

        if link_type is None:
            link_type = await self.conn.scalar(db.link_types.insert().values(
                   name="order",
                   description="Links of orders with offers",).returning(
                       db.link_types.c.id))


        return link_type

