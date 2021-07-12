# -*- coding: UTF-8 -*-

import json
import pandas
import requests
from dependencies import tools
from constants import *
import scraper


class MainCrawler:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        df = pandas.read_excel(INPUT_FILE, na_filter=False)
        self.__keywords_dict = {
            'Titles': list(filter(None, df['Titles'].to_list())),
            'Soft Skills': list(filter(None, df['Soft Skills'].to_list())),
            'Technical Skills': list(filter(None, df['Technical Skills'].to_list())),
            'Certifications': list(filter(None, df['Certifications'].to_list())),
        }
        self.__result_list = []

    def crawl(self):
        try:
            self.__logger.info("Starting execution...")

            # create session
            session = requests.Session()
            session.headers.update(HEADERS)
            session.proxies.update({'http': f"http://{PARAMETERS['proxySocket']}",
                                    'https': f"http://{PARAMETERS['proxySocket']}"})

            # iterate over urls
            for job_url in URLS:
                self.__logger.info(f"Trying: {job_url}")

                # make requests
                req = session.get(job_url)
                if req.status_code == 200:
                    self.__logger.info(f"Extracting information...")

                    ''' Scraping '''
                    scraper_obj = scraper.Scraper()
                    self.__result_list.append(scraper_obj.scrape(json.loads(req.text), self.__keywords_dict))

            ''' Saving '''
            result_json = json.dumps(self.__result_list, ensure_ascii=False)

            # execution finished
            self.__logger.info("Finishing execution...")
        except Exception as e:
            self.__logger.error(f"::Main Crawler:: Error found; {e}")
