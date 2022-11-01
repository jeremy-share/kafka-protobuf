# Kafka Protobuf example

Example of Kafka with Protobuf (Protocol Buffers) with a simple producer and consumer

Shared in the hope it is helpful to somebody

## Running
```shell
make up-core
echo "Wait for a while and make sure everything starts"
make up-producer-consumer
echo "Ctrl+c to exit when ready"
make logs-producer-consumer
make stop
```
