#!/usr/bin/env bash

# zip up and deploy code to S3.

cd $(dirname "$0")/../..

aws s3 rm s3://aroussel-dev/code/un_data_aggregator/ --recursive --profile alex
aws s3 cp un_data_aggregator s3://aroussel-dev/code/un_data_aggregator/ --profile alex --recursive --exclude="*.pyc" --exclude="*.DS_Store" --exclude="*.ini"
aws s3 cp un_data_aggregator/config/s3_settings.production.ini s3://devfenixagent/spark/FenixDataScience/config/settings.ini --profile alex