import ConfigParser
import os

configs_dir = os.path.dirname(os.path.realpath(__file__))
s3_settings = ConfigParser.ConfigParser()

s3_settings.read('s3_settings.ini')
