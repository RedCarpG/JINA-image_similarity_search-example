#!/bin/bash

URL=""
OUTPUT_DIR="./data"
OUTPUT_FILENAME=$OUTPUT_DIR/data.json

mkdir -p $OUTPUT_DIR

wget -O $OUTPUT_FILENAME $URL
