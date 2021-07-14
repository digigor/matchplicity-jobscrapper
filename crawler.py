# -*- coding: UTF-8 -*-

import os
import csv
import json
import pandas
import requests
from concurrent.futures import ThreadPoolExecutor
from dependencies import tools
from constants import *
import scraper


class Crawler:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        df = pandas.read_excel(INPUT_FILE, na_filter=False)
        self.__keywords_dict = {
            'Titles': list(filter(None, df['Titles'].to_list())),
            'Soft Skills': list(filter(None, df['Soft Skills'].to_list())),
            'Technical Skills': list(filter(None, df['Technical Skills'].to_list())),
            'Certifications': list(filter(None, df['Certifications'].to_list())),
            'Majors': list(filter(None, df['Majors'].to_list()))
        }
        self.__result_list = []

    def run(self, job_urls):
        try:
            # self.__logger.info("Starting execution...")
            self.__logger.info(f"{len(job_urls)} jobs found")

            # create session
            session = requests.Session()
            session.headers.update(HEADERS)
            session.proxies.update({'http': f"http://{PARAMETERS['proxySocket']}",
                                    'https': f"http://{PARAMETERS['proxySocket']}"})

            with ThreadPoolExecutor() as executor:
                # iterate over urls
                for count, job_url in enumerate(job_urls):
                    executor.submit(self.crawl, session, count, job_url)

            # ''' Saving '''
            # result_json = json.dumps(self.__result_list, ensure_ascii=False)

            # execution finished
            # self.__logger.info("Finishing execution...")
        except Exception as e:
            self.__logger.error(f"::Crawler:: Error found; {e}")

    def crawl(self, session, count, job_url):
        try:
            self.__logger.info(f"{count + 1}: {job_url}; Extracting information...")
            # make requests
            req = session.get(job_url)
            if req.status_code == 200:
                ''' Scraping '''
                scraper_obj = scraper.Scraper()
                # self.__result_list.append(scraper_obj.scrape(json.loads(req.text), self.__keywords_dict))
                result_dict = scraper_obj.scrape(json.loads(req.text), self.__keywords_dict)

                ''' Saving '''
                self.save_csv(result_dict)
        except Exception as e:
            self.__logger.error(f"{count + 1}: {job_url}; Error found; {e}")

    def save_csv(self, values_dict):
        try:
            # open file
            with open('output.csv', mode='a', encoding='utf-8') as csv_file:
                headers = values_dict.keys()
                writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',', lineterminator='\n')

                # create headers
                if os.stat('output.csv').st_size == 0:
                    writer.writeheader()

                # save data
                writer.writerow(values_dict)
        except Exception as e:
            self.__logger.error(f"::Saver:: Error found; {e}")
            raise
