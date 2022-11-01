FROM python:3.10

RUN pip3 install --upgrade pip

RUN mkdir /opt/project
WORKDIR /opt/project

COPY requirements.in .

RUN pip3 install -r requirements.in

COPY src src
COPY protobuf protobuf
COPY entrypoint.sh .

CMD ["./entrypoint.sh"]
