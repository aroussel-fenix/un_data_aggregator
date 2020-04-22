import configparser
import os

print(os.path.dirname(os.path.realpath(__file__)))

configs_dir = os.path.dirname(os.path.realpath(__file__))
s3_settings = configparser.ConfigParser()

s3_settings.read(['%s/aws_settings.ini' % configs_dir])
