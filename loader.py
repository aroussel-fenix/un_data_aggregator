import pandas as pd
import boto3
from sqlalchemy import create_engine
import logging
from acquire_data.config import s3_settings

logging.basicConfig(level='INFO')

secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
access_key_id = s3_settings.get('aws', 'aws_access_key_id')
s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

# read in a single file as a test
data = pd.read_csv('s3://aroussel-dev/un_data/conflict_data_abw.csv')

# move these connection params to a file
db_connect_string = "{dialect}://{user}:{password}@{host}:{port}/{db}".format(
                    dialect='mysql+pymysql',
                    user='',
                    password='',
                    host='',
                    port='3306',
                    db='conflictdb')
conflictdb_engine = create_engine(db_connect_string)

to_drop = ['iso', 'event_id_cnty', 'event_id_no_cnty', 'year', 'time_precision', 'sub_event_type', 'actor1',
        'assoc_actor_1', 'inter1', 'actor2', 'assoc_actor_2', 'inter2',
        'interaction', 'region', 'admin1', 'admin2', 'admin3',
        'location', 'geo_precision', 'source', 'source_scale', 'notes']
data_v2 = data.drop(to_drop, axis=1)

data_v2.to_sql('conflicts', conflictdb_engine, index=False, if_exists='append', chunksize=50)
