import pandas as pd
import boto3
from config import s3_settings  # this is only created by by init when this file is run.

# get AWS credentials and create s3 resource
secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
access_key_id = s3_settings.get('aws', 'aws_access_key_id')
s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

# For now, this will be my example CSV, however logic to loop through all available CSVs will need to be added
csv_df = pd.read_csv('https://data.humdata.org/dataset/3e4136ce-83c0-4159-93e8-e926836e97ae/'
                     'resource/4bfbcada-68bd-4184-aa29-0af2fff0b08a/download/fts_requirements_funding_cluster_uga.csv',
                     header=1)

# output to CSV
csv_df.to_csv('../data/medicare-office-locations.csv')

# write data to S3
s3.upload_file('../data/medicare-office-locations.csv', 'aroussel-dev-bucket', 'medicare-office-locations.csv')


# TODO: use requests library in for loop to get a list of child CSV URLs that live under a list of different webpages
# E.g. HDX homepage -> Data -> CSVs -> single webpage -> list of CSVs in that webpage.


# Should it be OOP? Like Scraper() object? Different Scraping child objects can inheret from it depending on which
# category of data they want to scrape?





