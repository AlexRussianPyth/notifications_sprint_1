import json
import logging

import pika
import pika.exceptions

from src.core.config import settings

logger = logging.getLogger(__name__)


def publish(message, connection, queue):
    try:
        channel = connection.channel()
        channel.basic_publish(
            exchange=settings.rabbit.exchange,
            routing_key=queue,
            body=json.dumps(message),
        )
        logger.info('Message was published')
    except pika.exceptions.UnroutableError:
        logger.error('Message was returned')
