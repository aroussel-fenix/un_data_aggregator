import boto3
from botocore.exceptions import ClientError
# this is only created by init when this file is run.
from config import s3_settings
import requests
from bs4 import BeautifulSoup
import os
import logging
import wget
import pytz
from datetime import datetime

logging.basicConfig(level='INFO')


def generate_valid_urls():
    try:
        with open('valid_urls.txt', 'r') as f:
            result_list = f.read().splitlines()
    except FileNotFoundError:
        print("File not found. Generating list from HDX URLs.")
        page = requests.get('https://data.humdata.org/search?organization=acled&q=&ext_page_size=200')
        soup = BeautifulSoup(page.content, 'html.parser')
        result_list = []
        url_root = "https://data.humdata.org"
        with open('valid_urls.txt', 'w') as f:
            for a in soup.find_all("div", class_="dataset-heading"):
                result_list.append(url_root + a.find("a").get('href'))
                f.write("%s\n" % (url_root + a.find("a").get('href')))
    return result_list


def download_to_s3(url, client, session):
    full_url, file_name, latest_upload_date = get_page_info(url, session)
    if len(file_name) == 21:
        try:
            obj = client.head_object(Bucket=s3_settings.get('aws', 'bucket'), Key='data/{}'.format(file_name))
            logging.info("{} already exists in s3. Checking to see if it is up to date.".format(file_name))
            last_s3_upload = obj['LastModified']
            if last_s3_upload < latest_upload_date:
                logging.info("{} in s3 out of date, re-downloading and uploading".format(file_name))
                csv = wget.download(full_url, out='data/')
                client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
                                   'data/{}'.format(file_name))
            else:
                logging.info("{} in s3 up to date, no refresh needed".format(file_name))
        except ClientError as exc:
            if exc.response['Error']['Code'] == '404':
                logging.info("{} does not exist in s3. Uploading to s3".format(file_name))
                if os.path.isfile('data/{}'.format(file_name)):
                    logging.info("{} exists locally, uploading to s3".format(file_name))
                    client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
                                       'data/{}'.format(file_name))
                else:
                    logging.info("{} does not exist locally, downloading then uploading to s3".format(file_name))
                    csv = wget.download(full_url, out='data/')
                    client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
                                       'data/{}'.format(file_name))
    elif len(file_name) == 21:
        logging.warning("{} is not a valid file name and was not downloaded".format(file_name))


def get_page_info(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a = soup.find(
        "a", class_="btn btn-empty btn-empty-blue hdx-btn resource-url-analytics ga-download")
    b = a.get('href')
    url_root = "https://data.humdata.org"
    full_url = url_root + b
    file_name = b.rsplit('/', 1)[1]
    latest_upload_date_search = soup.find("span", class_="date")
    latest_upload_date_string = latest_upload_date_search.get('title').rsplit(',', 1)[0].replace(',', '')
    utc = pytz.UTC
    latest_upload_date = utc.localize(datetime.strptime(latest_upload_date_string, '%B %d %Y'))
    return full_url, file_name, latest_upload_date


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
            logging.info("checking URL: {}".format(url))
            download_to_s3(url, s3, my_session)
    return 0
