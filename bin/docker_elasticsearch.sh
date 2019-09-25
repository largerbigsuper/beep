#/bin/bash

VERSION=7.3.2
CLUSTER_NAME=beep

docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e discovery.type=single-node -e cluster.name=$CLUSTER_NAME  elasticsearch:$VERSION

