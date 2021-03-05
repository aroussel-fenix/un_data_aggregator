# import boto3
# from botocore.exceptions import ClientError
# this is only created by init when this file is run.
# from config import s3_settings
import requests
from bs4 import BeautifulSoup
import os
import logging
import wget
import pytz
from datetime import datetime

logging.basicConfig(level='INFO')


class Fetcher:

    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://data.humdata.org/dataset/fts-requirements-and-funding-data-for-uganda"

    def _generate_valid_urls(self):
        # try:
        #     with open('valid_urls.txt', 'r') as f:
        #         result_list = f.read().splitlines()
        # except FileNotFoundError:
        logging.warning("File not found. Generating list from HDX URLs")

        url = "https://data.humdata.org/dataset/fts-requirements-and-funding-data-for-uganda"

        a = self._get_page_info()

            # page = requests.get('https://data.humdata.org/dataset/fts-requirements-and-funding-data-for-uganda')
            # soup = BeautifulSoup(page.content, 'html.parser')
        #     result_list = []
        #     url_root = "https://data.humdata.org"
        #     with open('valid_urls.txt', 'w') as f:
        #         for a in soup.find_all("a", class_="ga-download"):
        #             filename = url_root + a.get('href')
        #             result_list.append(filename)
        #             f.write(f"{filename}\n")
        # return result_list


    def _download_to_s3(self, url, session):
        full_url, file_name, latest_upload_date = self._get_page_info(url, session)
        print(full_url, file_name, latest_upload_date)
        # if len(file_name) == 21:
        #     try:
        #         obj = client.head_object(Bucket=s3_settings.get('aws', 'bucket'), Key='data/{}'.format(file_name))
        #         logging.info("{} already exists in s3. Checking to see if it is up to date.".format(file_name))
        #         last_s3_upload = obj['LastModified']
        #         if last_s3_upload < latest_upload_date:
        #             logging.info("{} in s3 out of date, re-downloading and uploading".format(file_name))
        #             csv = wget.download(full_url, out='data/')
        #             client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
        #                             'data/{}'.format(file_name))
        #         else:
        #             logging.info("{} in s3 up to date, no refresh needed".format(file_name))
        #     except ClientError as exc:
        #         if exc.response['Error']['Code'] == '404':
        #             logging.info("{} does not exist in s3. Uploading to s3".format(file_name))
        #             if os.path.isfile('data/{}'.format(file_name)):
        #                 logging.info("{} exists locally, uploading to s3".format(file_name))
        #                 client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
        #                                 'data/{}'.format(file_name))
        #             else:
        #                 logging.info("{} does not exist locally, downloading then uploading to s3".format(file_name))
        #                 csv = wget.download(full_url, out='data/')
        #                 client.upload_file('data/{}'.format(file_name), s3_settings.get('aws', 'bucket'),
        #                                 'data/{}'.format(file_name))
        # elif len(file_name) == 21:
        #     logging.warning("{} is not a valid file name and was not downloaded".format(file_name))

    def _fetch_date_from_soup(self, soup):
        latest_upload_date_search = soup.find("div", class_="update-date")
        trimmed_text = "".join(line.strip() for line in latest_upload_date_search.get_text().split("\n"))
        split_text = trimmed_text.rsplit(':')
        q = datetime.strptime(split_text[1], '%d %B %Y')
        return q

    def _get_page_info(self):
        page = self.session.get(self.base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        url_root = "https://data.humdata.org"
        result_dict = {"files": [], "update_date": self._fetch_date_from_soup(soup)}
        for a_tag in soup.find_all("a", class_="ga-download"):
            filename = url_root + a_tag.get('href')
            result_dict['files'].append(filename) 
        
        # a = soup.find(
        #     "a", class_="btn btn-empty btn-empty-blue hdx-btn resource-url-analytics ga-download")
        # b = a.get('href')
        # url_root = "https://data.humdata.org"
        # full_url = url_root + b
        # file_name = b.rsplit('/', 1)[1]
        
        # latest_upload_date_string = latest_upload_date_search.get('title').rsplit(',', 1)[0].replace(',', '')
        # utc = pytz.UTC
        # latest_upload_date = utc.localize(datetime.strptime(latest_upload_date_string, '%B %d %Y'))
        # return full_url, file_name, latest_upload_date


    def run(self):
        logging.info("generating valid URLs...")
        valid_urls = self._generate_valid_urls()
        # if not os.path.isdir('data'):
        #     os.mkdir('data/')
        # with requests.Session() as my_session:
        #     for url in valid_urls:
        #         logging.info("checking URL: {}".format(url))
        #         self._download_to_s3(url, my_session)
        return 0


if __name__ == "__main__":
    Fetcher().run()    


