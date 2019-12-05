from datetime import date

import db
import telegram


class Message:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def create(self, email, message):
        entity_id = await self.conn.scalar(db.entities.insert().values(
                name='Message from %s'%email,
                date_created=date.today(),
                object='message',).returning(db.entities.c.id))

        await self.conn.scalar(db.messages.insert().values(
           entity_id=entity_id,
           email=email,
           message=message,
           status=0,
           ).returning(db.messages.c.id))

        await telegram.send('E-mail: %s\n%s'%(email, message))
