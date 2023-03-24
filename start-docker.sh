#!/bin/bash

set -a
if [ -f .env ]; then
  echo "Loading Environment Variables..."

  export $(cat .env | xargs)
fi
set +a

docker-compose up --build