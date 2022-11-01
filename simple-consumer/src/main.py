from os import getenv
import logging
from typing import Optional

from dotenv import load_dotenv
from os.path import realpath, dirname

import protobuf.detected_pb2 as detected_pb2
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer


def main():
    kafka_server = getenv("KAFKA_SERVER", "127.0.0.1:9092")
    kafka_topic = getenv("KAFKA_TOPIC", "detected")
    kafka_consumer_group_id = getenv("KAFKA_CONSUMER_GROUP_ID", "simple-consumer")

    logger.info("Using KAFKA_SERVER='%s', KAFKA_TOPIC='%s', KAFKA_CONSUMER_GROUP_ID='%s'", kafka_server, kafka_topic,
                kafka_consumer_group_id)

    protobuf_deserializer = ProtobufDeserializer(detected_pb2.Detected, {'use.deprecated.format': False})

    consumer_conf = {'bootstrap.servers': kafka_server, 'group.id': kafka_consumer_group_id,
                     'auto.offset.reset': "earliest"}

    consumer = Consumer(consumer_conf)
    consumer.subscribe([kafka_topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            # Note: 0's and nulls are not distinguishable in protobuf
            # https://stackoverflow.com/questions/47373976/why-is-my-protobuf-message-in-python-ignoring-zero-values
            detected: Optional[detected_pb2.Detected] = protobuf_deserializer(msg.value(),
                                                                              SerializationContext(kafka_topic,
                                                                                                   MessageField.VALUE))

            if detected is not None:
                logger.info("Detected record host='%s' at='%d' {car=%d, person=%d, cat=%d, dog=%d}", detected.host,
                            detected.at, detected.detections.car, detected.detections.person, detected.detections.cat,
                            detected.detections.dog)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    root_dir = realpath(dirname(realpath(__file__)) + "/..")
    load_dotenv(dotenv_path=f"{root_dir}/.env")
    logging.basicConfig(level=getenv("LOGLEVEL", "INFO").upper())
    main()
