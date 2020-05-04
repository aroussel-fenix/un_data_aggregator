#!/bin/bash
cd $(dirname "$0")/../..
sudo docker build -t fetcher un_data_aggregator/
sudo docker image ls
sudo docker run --rm fetcher
