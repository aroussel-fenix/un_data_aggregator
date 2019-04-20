from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages mysql:mysql-connector-java:8.0.11 pyspark-shell'

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sc = spark.sparkContext
lines = sc.textFile("/Users/alexroussel/spark-2.3.1-bin-hadoop2.7/examples/src/main/resources/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: (p[0], p[1].strip()))
schemaString = "name age"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

schemaPeople = spark.createDataFrame(people, schema)

# CREATE TABLE needs to be happen before data is written. It needs an empty table.

schemaPeople.write.format('jdbc').options(
            url='jdbc:mysql://localhost/airflow?characterEncoding=latin1&useSSL=false',
            driver='com.mysql.jdbc.Driver',
            dbtable='test',
            user='airflow',
            password='airflow_password').mode('append').save()


read_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost/airflow?characterEncoding=latin1&useSSL=false") \
    .option("driver", "driver='com.mysql.jdbc.Driver'") \
    .option("dbtable", "test") \
    .option("user", "airflow") \
    .option("password", "airflow_password") \
    .load()

read_df2 = spark.read \
    .jdbc("jdbc:mysql://localhost/airflow", "airflow.test",
          properties={"user": "airflow", "password": "airflow_password"})
