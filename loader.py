import pandas as pd
from sqlalchemy import create_engine
import logging
from acquire_data.config import s3_settings

logging.basicConfig(level='INFO')


def lambda_handler(event, context):
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
    temp_table_name = 'conflicts_temp_{}'.format(updated_file.rsplit('_', 1)[1].split('.')[0])
    to_drop = ['iso', 'event_id_no_cnty', 'year', 'time_precision', 'sub_event_type', 'actor1',
               'assoc_actor_1', 'inter1', 'actor2', 'assoc_actor_2', 'inter2',
               'interaction', 'region', 'admin1', 'admin2', 'admin3',
               'location', 'geo_precision', 'source', 'source_scale', 'notes']
    data = data.drop(to_drop, axis=1)
    data = data.drop(data.index[0])
    data.to_sql(temp_table_name, conflictdb_engine, index=False, if_exists='replace', chunksize=50)
    conflictdb_engine.execute(
        "INSERT IGNORE INTO conflicts SELECT *, CURTIME() as inserted_at FROM {};".format(temp_table_name))
    conflictdb_engine.execute("DROP TABLE {};".format(temp_table_name))
    return 0
