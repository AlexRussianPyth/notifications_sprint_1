import uuid
import datetime as dt

from psycopg2.extensions import connection
import psycopg2.extras

from src.models.models import Notification
from src.db.abstract_database_service import AbstractNotificationDatabaseService


class NotificationPostgresService(AbstractNotificationDatabaseService):
    """Управляет взаимодействием с БД POstgreSQL"""
    def __init__(self, connection: connection, tablename: str):
        self.connection = connection
        self.tablename = tablename
        psycopg2.extras.register_uuid()  # Позволяет сервису принимать uuid в качестве параметров

    def _execute_query(self, query: str, values=None):
        """Выполняет SQL запрос и возвращает результат запроса"""
        with self.connection.cursor() as curs:
            if values:
                curs.execute(query, values)
            else:
                curs.execute(query)
                result = curs.fetchall()
                return result

    def save_notification_to_db(self, notification: Notification) -> None:
        """Сохраняет уведомление в БД"""
        query = f'''INSERT INTO {self.tablename} (notification_id, user_id, content_id, type, created_at)
                    VALUES (%s, %s, %s, %s, %s);'''
        values = (
                notification.notification_id,
                notification.user_id,
                notification.content_id,
                notification.type,
                str(dt.datetime.now()).split('.')[0]
                )
        self._execute_query(query, values)

    def get_notifications(self):
        """Возвращает все уведомления из БД"""
        query = f"SELECT * FROM notifications;"
        result = self._execute_query(query)

        return result

    def get_notification_by_id(self, notification_id: uuid.UUID, user_id: uuid.UUID):
        """Возвращает уведомление по notification_id"""
        query = f"""SELECT * FROM notifications
                  WHERE notification_id='{notification_id}' AND user_id='{user_id}';"""

        result = self._execute_query(query)
        return result[0] if result else None
