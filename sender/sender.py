from psycopg2.extras import DictCursor

from src.core.config import postgres_settings, rabbit_settings
from src.db.connections import create_pg_conn
from src.services.postgres_service import NotificationPostgresService
from src.services.worker import Worker
from src.senders.email_sender import EmailSender
from src.core.config import email_server_settings
from src.models.models import EmailTemplate


if __name__ == '__main__':
    with create_pg_conn(**postgres_settings.dict(), cursor_factory=DictCursor) as pg_conn:
        # Подключаемся к БД
        postgres_service = NotificationPostgresService(connection=pg_conn, tablename='notifications')
        # Инициализируем сервис отправки писем
        email_sender = EmailSender(email_server_settings, postgres_service)
        # Подключаемся к очереди в Rabbit и принимаем сообщения из очереди
        Worker(rabbit_settings, email_sender, EmailTemplate)
