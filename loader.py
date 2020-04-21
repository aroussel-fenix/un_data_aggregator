import pandas as pd
import boto3
import json
from web_scraper.config import s3_settings

# take file (from s3 normally) but will test with local file and load into DynamoDB table.

# This should work in Lambda, using an S3 trigger to load each file into DynamoDB.

# Build the connection to the DynamoDB table
secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
access_key_id = s3_settings.get('aws', 'aws_access_key_id')
dynamo_db = boto3.resource('dynamodb', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                           region_name='us-east-2')
table = dynamo_db.Table('conflict_data')

test_df = pd.read_csv('web_scraper/tmp/conflict_data_tun.csv', header=0)
test_df_v2 = test_df.drop(test_df.index[0])
for i in test_df_v2.columns:
    test_df_v2[i] = test_df_v2[i].astype(str)

# print(test_df_v2.transpose().to_dict().values())

test_json = test_df_v2.iloc[0].to_json()
# test_json_v2 = test_df_v2[['data_id', 'timestamp']].iloc[0].to_json()
test_json_v3 = json.loads(test_json)
# print(test_json_v3.__sizeof__())
with table.batch_writer() as batch:
    batch.put_item(test_json_v3)
