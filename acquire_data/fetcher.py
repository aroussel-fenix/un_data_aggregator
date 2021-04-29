import json
import logging
import os
from datetime import datetime

import requests

from acquire_data.config import settings

logging.basicConfig(level="INFO")


class Fetcher:
    def __init__(self):
        self.session = requests.Session()
        self.target_url = self._construct_url()
        self.filepath = f"acquire_data/data/{datetime.today().strftime('%Y-%m-%d')}-data.json"

    def _construct_url(self):
        result_url = settings.get("url", "base_url")
        result_url += "".join(
            x + "=" + settings.get("url", x)
            for x in settings["url"]
            if x in ["key", "email"]
        )
        return result_url

    def _download_file(self):
        response = self.session.get(self.target_url)
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file_p:
                json.dump(response.json(), file_p, ensure_ascii=False, indent=4)
        else:
            logging.info(f"{self.filepath} already in data folder")

    def _load_files_into_db(self):
        pass

    def run(self):
        logging.info(f"downloading files from {self.target_url}")
        self._download_file()
        self._load_files_into_db()
