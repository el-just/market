from datetime import date

import db
import telegram

from email.mime.text import MIMEText
from email.message import EmailMessage
import aiosmtplib

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

        await self.send_email(message, 'Message from %s'%email)


    async def send_email(self, text, subject):
        message = EmailMessage()
        message["From"] = os.environ['MARKET_MAIL_ORG']
        message["To"] = os.environ['MARKET_MAIL_SUPPORT']
        message["Subject"] = subject
        message.set_content(text)

        await aiosmtplib.send(
                message,
                hostname="smtp.yandex.ru",
                port=465,
                username=os.environ['MARKET_MAIL_ORG'],
                password=os.environ['MARKET_MAIL_ORG_PASSWORD'],
                use_tls=True,
                validate_certs=False,
                )
