from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('app2').setMaster('local')
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
print("5 element array has {} partitions".format(distData.getNumPartitions()))
print("Sum of list is {}".format(distData.reduce(lambda a, b: a + b)))

distFile = sc.textFile("tmy3-solar/tmy3.csv")
print("CSV has {} partitions".format(distFile.getNumPartitions()))

distFile.map(lambda s: len(s)).reduce(lambda a, b: a + b)

# trying to understand map -> reduce by using string example
strings = ['aaa', 'aaaaa', 'aa', 'aaaaaaaa', 'aaaaaaaaa']
distStrings = sc.parallelize(strings)
distStrings.map(lambda s: len(s)).reduce(lambda a, b: a + b)

distStrings.collect()
print distStrings.take(5)
