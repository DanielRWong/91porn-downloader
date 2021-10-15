# -*- coding: utf-8 -*-

import cfscrape
from retrying import retry

from config.config import *

class CFDownloader(object):
    def __init__(self):
        super().__init__()
        self.scraper = cfscrape.create_scraper()

    @retry(stop_max_attempt_number=5)
    def cfdownload(self, url):
        return self.scraper.get(url=url, headers=headers).text