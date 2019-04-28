from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
import os
from web_scraper.config import s3_settings  # this is only created by by init when this file is run.

spark_path = '/Users/alexroussel/spark-2.3.1-bin-hadoop2.7'
os.environ['SPARK_HOME'] = spark_path
os.environ['HADOOP_HOME'] = spark_path
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages mysql:mysql-connector-java:8.0.11 pyspark-shell'

access_key_id = s3_settings.get('aws', 'aws_access_key_id')
secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')

spark = SparkSession \
    .builder \
    .appName("PySpark ETL") \
    .config("spark.hadoop.fs.s3a.access.key", access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_access_key) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

sc = spark.sparkContext

rdd = sc.textFile("s3a://aroussel-dev-bucket/medicare-office-locations.csv")
rdd.count()

# TODO code below to read csv into relational DB
# parts = lines.map(lambda l: l.split(","))
# people = parts.map(lambda p: (p[0], p[1].strip()))
# schemaString = "name age"
# fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
# schema = StructType(fields)
#
# schemaPeople = spark.createDataFrame(people, schema)

# CREATE TABLE needs to happen before data is written. It needs an empty table.

# schemaPeople.write.format('jdbc').options(
#             url='jdbc:mysql://localhost/airflow?characterEncoding=latin1&useSSL=false',
#             driver='com.mysql.jdbc.Driver',
#             dbtable='test',
#             user='airflow',
#             password='airflow_password').mode('append').save()
#
#
# read_df = spark.read \
#     .format("jdbc") \
#     .option("url", "jdbc:mysql://localhost/airflow?characterEncoding=latin1&useSSL=false") \
#     .option("driver", "driver='com.mysql.jdbc.Driver'") \
#     .option("dbtable", "test") \
#     .option("user", "airflow") \
#     .option("password", "airflow_password") \
#     .load()
#
# read_df2 = spark.read \
#     .jdbc("jdbc:mysql://localhost/airflow", "airflow.test",
#           properties={"user": "airflow", "password": "airflow_password"})
