#!/bin/sh

# create prometheus folder
mkdir prometheus/prom
chmod 777 prometheus/prom
echo Created persistent prometheus volume

# create grafana folder
mkdir grafana/grafana-storage
chown 472 grafana/grafana-storage
echo Created persistent grafana volume
