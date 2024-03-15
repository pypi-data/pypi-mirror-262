"""
Test cases for the KafkaBroker class.

The tests are run against a Kafka broker running in a Docker container. If the container
is not running, it will be started before the running the test and stopped after the 
tests are done.
"""

import os
import pytest
from pathlib import Path
from time import sleep
from kafka.admin import NewTopic
from posted import NoMsg
from posted.tests.utils import service_is_running, start_service, stop_service
from posted.tests.common import (
    EXISTING_CHANNEL,
    gen_test_mk_msg_broker_args,
    base_test_on_demand_consumption,
    base_test_reactive_consumption,
)

from kafkaposted.base import KafkaBroker

SERVICE_CONTAINER_NAME = 'kafkaposted_test'
DOCKER_COMPOSE_FILEPATH = Path(
    os.path.dirname(os.path.abspath(__file__)), 'docker-compose.yml'
)


@pytest.fixture(scope='session', autouse=True)
def ensure_service_is_running():
    if service_is_running(SERVICE_CONTAINER_NAME):
        yield
    else:
        start_service(SERVICE_CONTAINER_NAME, DOCKER_COMPOSE_FILEPATH)
        try:
            yield
        finally:
            stop_service(SERVICE_CONTAINER_NAME, DOCKER_COMPOSE_FILEPATH)


@pytest.fixture(scope='module')
def broker():
    return KafkaBroker(bootstrap_servers='localhost:9093')


@pytest.fixture(autouse=True)
def init_testing_data(broker: KafkaBroker):
    topics = broker._admin.list_topics()
    if topics:
        broker._admin.delete_topics(topics)
        sleep(0.2)
    broker._admin.create_topics(
        [NewTopic(name=EXISTING_CHANNEL, num_partitions=1, replication_factor=1)]
    )


@pytest.mark.parametrize(
    'message, channel', list(gen_test_mk_msg_broker_args()),
)
def test_on_demand_consumption(broker: KafkaBroker, message, channel):
    base_test_on_demand_consumption(broker, message, channel)


@pytest.mark.parametrize(
    'message, channel', list(gen_test_mk_msg_broker_args()),
)
def test_reactive_consumption(broker: KafkaBroker, message, channel):
    base_test_reactive_consumption(broker, message, channel)
