#!/bin/bash

SCRIPT_PATH=$(dirname $(realpath -s $0))

docker run --rm -it \
  -v $SCRIPT_PATH/data:/data \
  -v $SCRIPT_PATH/src:/app \
  smartplugmon /bin/bash --rcfile /bashrc

