from psycopg2.extras import DictCursor

from src.core.config import postgres_settings, rabbit_settings
from src.db.connections import create_pg_conn
from src.db.postgres import PostgresService
from src.db.rabbit.connection import RabbitConsumer
from src.services.email_service import EmailSender
from src.core.config import email_server_settings
from src.models.models import EmailTemplate



import pika

RECIPIENT_EMAILS = ['durden191@yandex.ru', 'alexvkleschov@gmail.com']


if __name__ == '__main__':
    email_sender = EmailSender(email_server_settings)
    foo = RabbitConsumer(rabbit_settings, email_sender)


    '''
    with create_pg_conn(**postgres_settings.dict(), cursor_factory=DictCursor) as pg_conn:
        # Подключения к БД и почтовому серверу
    
        postgres_service = PostgresService(pg_conn=pg_conn, tablename='notifications')
        server = get_smtp_server_connection(**email_server_settings.dict())

        # Отправляем письмо
        with open('test_template.html') as f:
            send_html_email(server, email_server_settings.login, RECIPIENT_EMAILS, 'New Letter Test', f.read())

          # Закрываете соединение с smtp-сервером

        # '''