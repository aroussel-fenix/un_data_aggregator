import ConfigParser
import os

print os.path.dirname(os.path.realpath(__file__))

configs_dir = os.path.dirname(os.path.realpath(__file__))
s3_settings = ConfigParser.ConfigParser()

s3_settings.read(['%s/s3_settings.ini' % configs_dir])
