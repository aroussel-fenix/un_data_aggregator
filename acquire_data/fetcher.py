import pandas as pd
import boto3
# this is only created by init when this file is run.
from config import s3_settings
import requests
from bs4 import BeautifulSoup
import json
import pickle
import os
import logging
import wget

logging.basicConfig(level='INFO')


def generate_valid_urls():
    try:
        with open("valid_urls.txt", "rb") as fp:
            result_list = pickle.load(fp)
    except FileNotFoundError:
        print("File not found. Generating list from HDX URLs. This may take a few minutes.")
        iso_dict = {}
        result_list = []
        with open('iso3.json') as json_file:
            iso_list = json.load(json_file)
        for i in iso_list:
            iso_dict.update({i['name']: i['iso3']})
        parent_url_root = 'https://data.humdata.org/dataset/acled-data-for-'
        for x in iso_dict.keys():
            if requests.head(parent_url_root + x).status_code == 200:
                result_list.append(parent_url_root + x)
    return result_list


def download_to_s3(url, client):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a = soup.find(
        "a", class_="btn btn-empty btn-empty-blue hdx-btn resource-url-analytics ga-download")
    b = a.get('href')
    url_root = "https://data.humdata.org"
    file_name = b.rsplit('/', 1)[1]

    try:
        csv = wget.download(url_root + b, out='data/')
    except ConnectionError:
        logging.error("CSV download failed.")
    try:
        client.upload_file('data/{}'.format(file_name), 'aroussel-dev', 'data/{}'.format(file_name))
    except ConnectionError:
        logging.error("Upload to S3 failed.")


def run():
    # get AWS credentials and create s3 client
    secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
    access_key_id = s3_settings.get('aws', 'aws_access_key_id')
    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    valid_urls = generate_valid_urls()
    if not os.path.isdir('data'):
        os.mkdir('data/')
    for url in valid_urls:
        download_to_s3(url, s3)
    return 0
