# -*- coding: UTF-8 -*-

import json
import pandas
from concurrent.futures import ThreadPoolExecutor
from dependencies import tools
from config import *
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
            self.__logger.info("Starting execution")

            # create session
            session = self.__tools_obj.create_session()

            with ThreadPoolExecutor() as executor:
                # iterate over urls
                for count, job_url in enumerate(job_urls):
                    executor.submit(self.crawl, session, count, job_url)

            # execution finished
            self.__logger.info("Finishing execution")
            return self.__result_list
        except Exception as e:
            self.__logger.error(f"::Crawler:: Error found; {e}")
            return self.__result_list

    def crawl(self, session, count, job_url):
        try:
            self.__logger.info(f"Job {count + 1} - \"{job_url}\": Extracting information")

            # make requests
            req = session.get(job_url)
            if req.status_code == 200:
                ''' Scraping '''
                scraper_obj = scraper.Scraper()
                self.__result_list.append(scraper_obj.scrape(json.loads(req.text), self.__keywords_dict))
            else:
                # error job url
                self.__logger.error(f"Status Code Error: {req.status_code}; Url: {req.url}")

        except Exception as e:
            self.__logger.error(f"Job {count + 1} - {job_url}; Error found; {e}")
