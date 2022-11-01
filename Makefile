networks:
	docker network create kafka-protobuf-main || true

protobuf-compile:
	protoc --python_out=./protobuf -I=protobuf protobuf/detected.proto
	rm -rf simple-consumer/protobuf
	cp -rp protobuf simple-consumer/protobuf
	rm -rf simple-producer/protobuf
	cp -rp protobuf simple-producer/protobuf

up:
	make networks
	docker-compose build --pull
	docker-compose up -d

up-core:
	make networks
	docker-compose up -d zookeeper kafka1 schemaregistry

up-producer-consumer:
	docker-compose up -d simple-producer simple-consumer

down:
	docker-compose down

stop:
	make down

logs:
	docker-compose logs -f

logs-producer-consumer:
	docker-compose logs -f simple-producer simple-consumer

ps:
	docker-compose ps
