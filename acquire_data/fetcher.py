import logging
import os
from datetime import datetime

import requests
import wget
from bs4 import BeautifulSoup
from config import settings

logging.basicConfig(level="INFO")


class Fetcher:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings["urls"]["target_url"]

    def _download_files(self):
        url_dict = self._get_page_info()
        for url in url_dict["files"]:
            filename = url.rsplit("/", 1)[1]
            if not os.path.isfile("data/{}".format(filename)):
                wget.download(url, out="data/")
            else:
                logging.info(f"{filename} already in data folder")

    def _fetch_date_from_soup(self, soup):
        latest_upload_date_search = soup.find("div", class_="update-date")
        trimmed_text = "".join(
            line.strip() for line in latest_upload_date_search.get_text().split("\n")
        )
        split_text = trimmed_text.rsplit(":")
        q = datetime.strptime(split_text[1], "%d %B %Y")
        return q

    def _get_page_info(self):
        page = self.session.get(self.base_url)
        soup = BeautifulSoup(page.content, "html.parser")
        url_root = "https://data.humdata.org"
        result_dict = {"files": [], "update_date": self._fetch_date_from_soup(soup)}
        for a_tag in soup.find_all("a", class_="ga-download"):
            filename = url_root + a_tag.get("href")
            logging.info(f"found {filename}. Adding to list.")
            result_dict["files"].append(filename)
        return result_dict

    def _load_files_into_db(self):
        pass

    def run(self):
        logging.info(f"downloading files from {self.base_url}")
        self._download_files()
        self._load_files_into_db()
