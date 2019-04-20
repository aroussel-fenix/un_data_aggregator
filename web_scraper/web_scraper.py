import pandas as pd
import boto3
from config import s3_settings

test = pd.read_csv('https://data.humdata.org/dataset/'
                   '3e4136ce-83c0-4159-93e8-e926836e97ae/'
                   'resource/4bfbcada-68bd-4184-aa29-0af2fff0b08a/download/'
                   'fts_requirements_funding_cluster_uga.csv', header=1)


# TODO: use requests library in for loop to get a list of child CSV URLs that live under a list of different webpages
# E.g. HDX homepage -> Data -> CSVs -> single webpage -> list of CSVs in that webpage.

access_key = s3_settings.get('aws', 'aws_access_key_id')
access_key_id = s3_settings.get('aws', 'aws_secret_access_key_id')

s3 = boto3.client('s3')
s3.list_objects(Bucket='my_bucket_name', Prefix=path + serial)


# Should it be OOP? Like Scraper() object? Different Scraping child objects can inheret from it depending on which
# category of data they want to scrape?





