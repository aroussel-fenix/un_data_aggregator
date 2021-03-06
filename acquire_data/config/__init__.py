import configparser
import os

configs_dir = os.path.dirname(os.path.realpath(__file__))
settings = configparser.ConfigParser()

settings.read(['%s/settings.ini' % configs_dir])
