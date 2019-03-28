from pyspark.sql import SparkSession

logFile = "/Users/alexroussel/spark-2.3.1-bin-hadoop2.7/README.md"
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()
print "Lines with a: %i, lines with b: %i" % (numAs, numBs)

spark.stop()



#TODO read in csvs to pyspark




#TODO data manipulation in pyspark


#TODO how does this sit in an ETL pipeline? S3 -> PySpark -> local MySQL DB?


#TODO how would you scale this solution?

