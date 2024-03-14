"""
Base module for Apache Kafka message broker.

This module provides an implementation of the `MsgBrokerBase` interface for Apache Kafka.
The broker is implemented using the `kafka-python` package. The broker is designed to be
used in a multi-threaded environment, and it uses a thread pool to consume messages from
the Kafka topics.
"""

from functools import cached_property, lru_cache
import threading
from typing import Any, Callable
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from posted import MsgBrokerBase, NoMsg


class KafkaBroker(MsgBrokerBase):
    """
    Message broker for Apache Kafka.
    """

    def write(self, channel: str, message: Any):
        if channel not in self._admin.list_topics():
            self._admin.create_topics(
                [NewTopic(name=channel, num_partitions=1, replication_factor=1)]
            )
            assert self.read(channel) == NoMsg  # validate topic creation
        kwargs = dict(value=message)
        if message is None:
            kwargs[
                'key'
            ] = b''  # kafka-python does not allow (None, None) as a key-value pair
        future = self._producer.send(channel, **kwargs)
        future.get(timeout=60)

    def read(self, channel: str):
        if channel not in self._admin.list_topics():
            return NoMsg
        consumer = self._mk_consumer(channel, consumer_timeout_ms=500)
        try:
            return next(consumer).value
        except StopIteration:
            return NoMsg

    def subscribe(self, channel: str, callback: Callable[[Any], None]):
        def consume(stop_event):
            consumer = self._mk_consumer(
                channel, consumer_timeout_ms=100, auto_offset_reset='earliest'
            )
            while not stop_event.is_set():
                try:
                    msg = next(consumer).value
                    callback(msg)
                except StopIteration:
                    pass  # No message, continue the loop

        stop_event = threading.Event()
        self._subscriptions.setdefault(channel, []).append(stop_event)
        self._executor.submit(consume, stop_event)

    def unsubscribe(self, channel: str):
        for sub in self._subscriptions.get(channel, []):
            sub.set()
        self._subscriptions.pop(channel, None)

    @cached_property
    def _admin(self):
        return KafkaAdminClient(**self._config)

    @cached_property
    def _producer(self):
        config = {'value_serializer': self._encoder, **self._config}
        return KafkaProducer(**config)

    @lru_cache
    def _mk_consumer(self, channel: str, **kwargs):
        config = {'value_deserializer': self._decoder, **kwargs, **self._config}
        return KafkaConsumer(channel, **config)
