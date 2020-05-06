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
    updated_path = 's3://{}/'.format(s3_settings.get('aws', 'bucket')) + updated_file
    data = pd.read_csv(updated_path)
    temp_table_name = 'conflicts_temp_{}'.format(updated_file.rsplit('_', 1)[1].split('.')[0])
    to_drop = ['iso', 'event_id_no_cnty', 'year', 'time_precision', 'sub_event_type', 'actor1',
               'assoc_actor_1', 'inter1', 'actor2', 'assoc_actor_2', 'inter2',
               'interaction', 'region', 'admin1', 'admin2', 'admin3', 'geo_precision', 'source_scale']
    data = data.drop(to_drop, axis=1)
    data = data.drop(data.index[0])
    data.to_sql(temp_table_name, conflictdb_engine, index=False, if_exists='replace', chunksize=50)
    conflictdb_engine.execute("""
    CREATE TABLE IF NOT EXISTS `conflicts` (
      `data_id` double DEFAULT NULL,
      `event_id_cnty` varchar(255) NOT NULL,
      `event_date` date DEFAULT NULL,
      `event_type` varchar(255) DEFAULT NULL,
      `country` varchar(255) DEFAULT NULL,
      `location` varchar(255) DEFAULT NULL,
      `latitude` varchar(255) DEFAULT NULL,
      `longitude` varchar(255) DEFAULT NULL,
      `source` varchar(255) DEFAULT NULL,
      `notes` text DEFAULT NULL,
      `fatalities` int(11) DEFAULT NULL,
      `timestamp` double DEFAULT NULL,
      `iso3` varchar(4) DEFAULT NULL,
      `inserted_at` datetime DEFAULT NULL,
      PRIMARY KEY (`event_id_cnty`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    """)
    conflictdb_engine.execute(
        "INSERT IGNORE INTO conflicts SELECT *, CURTIME() as inserted_at FROM {};".format(temp_table_name))
    conflictdb_engine.execute("DROP TABLE {};".format(temp_table_name))
    return 0
