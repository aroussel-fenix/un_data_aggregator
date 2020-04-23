import pandas as pd
import boto3
from sqlalchemy import create_engine
import logging
from acquire_data.config import s3_settings

logging.basicConfig(level='INFO')

def lambda_handler(event, context):
    secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
    access_key_id = s3_settings.get('aws', 'aws_access_key_id')
    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    db_connect_string = "{dialect}://{user}:{password}@{host}:{port}/{db}".format(
                        dialect='mysql+pymysql',
                        user=s3_settings.get('conflictdb', 'user'),
                        password=s3_settings.get('conflictdb', 'password'),
                        host=s3_settings.get('conflictdb', 'host'),
                        port=s3_settings.get('conflictdb', 'port'),
                        db=s3_settings.get('conflictdb', 'db'))
    conflictdb_engine = create_engine(db_connect_string)

    updated_file = event['Records'][0]['s3']['object']['key']
    updated_path = 's3://aroussel-dev/' + updated_file
    data = pd.read_csv(updated_path)

    to_drop = ['iso', 'event_id_cnty', 'event_id_no_cnty', 'year', 'time_precision', 'sub_event_type', 'actor1',
            'assoc_actor_1', 'inter1', 'actor2', 'assoc_actor_2', 'inter2',
            'interaction', 'region', 'admin1', 'admin2', 'admin3',
            'location', 'geo_precision', 'source', 'source_scale', 'notes']
    data_v2 = data.drop(to_drop, axis=1)
    data_v3 = data_v2.drop(data_v2.index[0])
    data_v3.to_sql('conflicts', conflictdb_engine, index=False, if_exists='append', chunksize=50)

    return 0