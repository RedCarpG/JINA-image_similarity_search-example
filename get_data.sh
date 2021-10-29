#!/bin/bash


DATASET="arnaud58/landscape-pictures"
FILE="landscape-pictures.zip"
DATA_DIR="data/images"

if [ -d ${DATA_DIR} ]; then
  echo ${DATA_DIR}' already exists'
  exit 1
fi

mkdir -p ${DATA_DIR} && \

cd ${DATA_DIR}

kaggle datasets download -d ${DATASET} && \
unzip -q ${FILE} && \
rm ${FILE}

cd ..