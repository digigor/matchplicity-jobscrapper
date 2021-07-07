# -*- coding: UTF-8 -*-

import json
import requests
from dependencies import tools
from constants import *
import scraper


class MainCrawler:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()

    def crawl(self):
        try:
            self.__logger.info("Starting execution...")

            job_url = 'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/MA-Boston/Programs---Product-Line-Officer_JR2101885-1'
            req = requests.get(job_url)
            if req.status_code == 200:
                ''' Scraping '''
                scraper_obj = scraper.Scraper()
                result_dict = scraper_obj.scrape(req.text, job_url)

                ''' Saving '''
                result_json = json.dumps(result_dict, ensure_ascii=False)

            # execution finished
            self.__logger.info("Finishing execution...")
        except Exception as e:
            self.__logger.error(f"::Main Crawler:: Error found; {e}")
