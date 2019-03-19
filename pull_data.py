import wget
import boto3

# pull down some example data
print('Beginning file download with wget module')

url = 'https://data.humdata.org/dataset/3e4136ce-83c0-4159-93e8-e926836e97ae/resource/51499c1a-574e-40ea-9947-' \
      '15815d82b144/download/fts_requirements_funding_uga.csv'
wget.download(url, '/Users/alexroussel/PycharmProjects/un_data_aggregator/test.csv')

# move the CSV to S3 bucket
s3 = boto3.client('s3')
s3.list_objects(Bucket='my_bucket_name', Prefix=path + serial)
