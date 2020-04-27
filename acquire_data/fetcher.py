import boto3
from botocore.exceptions import ClientError
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
        logging.warn("File not found. Generating list from HDX URLs. This may take a few minutes.")
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


def download_to_s3(url, client, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a = soup.find(
        "a", class_="btn btn-empty btn-empty-blue hdx-btn resource-url-analytics ga-download")
    b = a.get('href')
    url_root = "https://data.humdata.org"
    file_name = b.rsplit('/', 1)[1]

    if len(file_name) == 21:
        # csv = wget.download(url_root + b, out='data/')
        try:
            obj = client.head_object(Bucket='aroussel-dev', Key='data/{}'.format(file_name))
            logging.info("{} already exists in s3. Not uploading.".format(file_name))
        except ClientError as exc:
            if exc.response['Error']['Code'] == '404':
                logging.info("{} does not exist in s3. Uploading to s3".format(file_name))
                if os.path.isfile('data/{}'.format(file_name)):
                    logging.info("{} exists locally, uploading to s3".format(file_name))
                    client.upload_file('data/{}'.format(file_name), 'aroussel-dev', 'data/{}'.format(file_name))
                else:
                    logging.info("{} does not exist locally, downloading then uploading to s3".format(file_name))
                    csv = wget.download(url_root + b, out='data/')
                    client.upload_file('data/{}'.format(file_name), 'aroussel-dev', 'data/{}'.format(file_name))
    # elif os.path.isfile('data/{}'.format(file_name)):
    #     logging.info("{} already exists locally and was not downloaded".format(file_name))
    elif len(file_name) == 21:
        logging.warn("{} is not a valid file name and was not downloaded".format(file_name))

def run():
    secret_access_key = s3_settings.get('aws', 'aws_secret_access_key')
    access_key_id = s3_settings.get('aws', 'aws_access_key_id')
    logging.info("creating s3 client...")
    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    logging.info("generating valid URLs...")
    valid_urls = generate_valid_urls()
    if not os.path.isdir('data'):
        os.mkdir('data/')
    with requests.Session() as my_session:
        for url in valid_urls:
            logging.info("downloading {}".format(url))
            download_to_s3(url, s3, my_session)
    return 0
