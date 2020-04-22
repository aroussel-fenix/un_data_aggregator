from pyspark.sql import SQLContext
from pyspark import SparkContext
from datetime import datetime
import os
import logging
from acquire_data.config import s3_settings  # this is only created by init when this file is run.

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages mysql:mysql-connector-java:8.0.11,' \
                                    'com.amazonaws:aws-java-sdk:1.10.34,org.apache.hadoop:hadoop-aws:2.7.0 pyspark-shell'

access_key_id = s3_settings.get('aws', 'aws_access_key_id')
secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')

sc = SparkContext.getOrCreate()

hadoopConf = sc._jsc.hadoopConfiguration()
hadoopConf.set("fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
hadoopConf.set("fs.s3.awsAccessKeyId", s3_settings.get('aws', 'aws_access_key_id'))
hadoopConf.set("fs.s3.awsSecretAccessKey", s3_settings.get('aws', 'aws_secret_access_key'))

sqlContext = SQLContext(sc)

rdd = sqlContext.read.csv("s3://aroussel-dev/medicare-office-locations*", inferSchema=True, header=True)

# For now write output back to S3
rdd.write.csv("s3://aroussel-dev/medicare-office-locations-output/%s" % (datetime.now().strftime("%Y-%m-%d_%H%M%S")))

# When ready to write to output DB, use code below
# rdd.write.format('jdbc').options(
#             url='jdbc:mysql://localhost/airflow?characterEncoding=latin1&useSSL=false&useLegacyDatetimeCode=false&serverTimezone=UTC',
#             driver='com.mysql.cj.jdbc.Driver',
#             dbtable='test',
#             user='airflow',
#             password='airflow_password').mode('append').save()
# logging.info("Done writing tmp to table...")
