#!/usr/bin/env bash

set -e

RUN_WORKERS=${RUN_WORKERS:-"2"}
RUN_HOST=${RUN_HOST:-"0.0.0.0"}
RUN_PORT=${RUN_PORT:-"80"}

gunicorn \
  --workers="${RUN_WORKERS}" \
  --bind="${RUN_HOST}:${RUN_PORT}" \
  src.main:app
