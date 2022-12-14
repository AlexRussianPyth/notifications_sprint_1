import json
import logging
from abc import ABC, abstractmethod

import pika
import pika.exceptions

from config.settings import RabbitMQSettings
from utils.backoff import backoff, backoff_reconnect

logger = logging.getLogger(__name__)


class Publisher(ABC):
    @abstractmethod
    def publish(self, message: dict, headers: dict) -> None:
        """Publish message to broker or sender."""
        pass


class RabbitPublisher(Publisher):

    def reconnect(self) -> None:
        try:
            self.connection.close()
        except BaseException:
            pass
        self.connect()

    @backoff()
    def connect(self) -> None:
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.params.queue, durable=True, exclusive=False, auto_delete=False)
        self.channel.confirm_delivery()

    def __init__(self, rabbit_params: RabbitMQSettings) -> None:
        self.params = rabbit_params
        credentials = pika.PlainCredentials(rabbit_params.username, rabbit_params.password)
        self.parameters = pika.ConnectionParameters(rabbit_params.host, rabbit_params.port, credentials=credentials)
        self.connect()

    @backoff_reconnect()
    def publish(self, message: dict, headers: dict) -> None:
        try:
            self.channel.basic_publish(exchange=self.params.exchange,
                                       routing_key=self.params.queue,
                                       body=json.dumps(message),
                                       properties=pika.BasicProperties(
                                           headers=headers,
                                           delivery_mode=pika.DeliveryMode.Transient),
                                       mandatory=True)
            logger.info('Message was published')
        except pika.exceptions.UnroutableError:
            logger.error('Message was returned')
