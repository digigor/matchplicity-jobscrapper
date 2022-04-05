# -*- coding: UTF-8 -*-
import re

import pandas
from concurrent.futures import ThreadPoolExecutor
from dependencies import tools
from config import *
from scrapers import myworkdayjobs, taleo , myworkdayjobs_fromapi
import json


class Crawler:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        df = pandas.read_excel(INPUT_FILE, na_filter=False)
        locations = pandas.read_csv(LOCATIONS_FILE, na_filter=False)
        
        self.__keywords_dict = {
            'Titles': list(filter(None, df['Titles'].to_list())),
            'Soft Skills': list(filter(None, df['Soft Skills'].to_list())),
            'Technical Skills': list(filter(None, df['Technical Skills'].to_list())),
            'Certifications': list(filter(None, df['Certifications'].to_list())),
            'Majors': list(filter(None, df['Majors'].to_list())),
            'locations': locations.to_dict('records')
        }
        self.__result_list = []

    def run(self, job_urls):
        try:
            self.__logger.info("Starting execution")

            # create session
            session = self.__tools_obj.create_session()

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: #TODO quitar el max_workers
                # iterate over urls
                for count, job_url in enumerate(job_urls):
                    executor.submit(self.crawl_requests, session, count, job_url['url'])

            # execution finished
            self.__logger.info("Finishing execution")
            return self.__result_list
        except Exception as e:
            self.__logger.error(f"::Crawler:: Error found; {e}")
            return self.__result_list

    def crawl_requests(self, session, count, job_url):
        try:
            results = {
                'title': None,
                'description': None,
                'application_url': job_url,
                'job_type': [],
                'job_locations': [],
                'preferred_years_experience': [],
                'preferred_previous_job_title': None,
                'salary': None,
                'preferred_certification': [],
                'preferred_soft_skill': [],
                'preferred_technical_skill': [],
                'job_preferred_major': [],
                'job_gpa': None,
                'success': None,
                'error_message': None,
                'source': None
            }
            df = pandas.read_excel(INPUT_FILE, na_filter=False)
            locations = pandas.read_csv(LOCATIONS_FILE, na_filter=False)
            keywords_dict = {
                'Titles': list(filter(None, df['Titles'].to_list())),
                'Soft Skills': list(filter(None, df['Soft Skills'].to_list())),
                'Technical Skills': list(filter(None, df['Technical Skills'].to_list())),
                'Certifications': list(filter(None, df['Certifications'].to_list())),
                'Majors': list(filter(None, df['Majors'].to_list())),
                'locations': locations.to_dict('records')
            }

            self.__logger.info(f"Job {count + 1} - \"{job_url}\": Extracting information")

            # Requests strategy
            # Agregar mas urls de Requests aqui
            if 'myworkdayjobs' in job_url:
                if 'abbott.wd5' in job_url:
                    results = myworkdayjobs.Scraper().scrape(job_url, session, keywords_dict)
                else:
                    results = myworkdayjobs_fromapi.Scraper().scrape(job_url, keywords_dict)


            # Selenium Strategy
            # Agregar mas urls de selenium aqui
            elif 'taleo' in job_url:
                results['source'] = 'taleo'
                if 'job=' in job_url:
                    driver = self.__tools_obj.create_driver()
                    driver.get(job_url)

                    results = taleo.Scraper().scrape(driver, self.__keywords_dict, job_url)
                    driver.close()
                else:
                    # No job id on url
                    results['success'] = False
                    results['error_message'] = 'Job Id missing or wrong.'

                #self.__result_list.append(results)

            else:
                results['success'] = False
                results['error_message'] = 'wrong web source'
                self.__logger.error(f"Wrong URL; Url: {job_url} ")

            self.__logger.info(f"Job {count + 1} - \"{job_url}\": Scraping finished")

            self.__result_list.append(results)
        except Exception as e:
            self.__logger.error(f"Job {count + 1} - {job_url}; Error found; {e}")
