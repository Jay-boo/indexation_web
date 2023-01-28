#!/bin/bash

docker build -t image_tp3 .

file="./results.json"

if ! test -e "$file"; then
  touch results.json
fi

docker run -v $(pwd)/results.json:/TPquery/results.json image_tp3
