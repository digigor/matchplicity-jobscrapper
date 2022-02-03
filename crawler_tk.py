# -*- coding: UTF-8 -*-
import re

import pandas
from concurrent.futures import ThreadPoolExecutor
from dependencies import tools
from config import *
from scrapers import myworkdayjobs, taleo
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
                'source': 'myworkdayjobs'
            }
            self.__logger.info(f"Job {count + 1} - \"{job_url}\": Extracting information")

            # Requests strategy
            # Agregar mas urls de Requests aqui
            if 'myworkdayjobs' in job_url:
                results['source'] = 'myworkdayjobs'
                req = session.get(job_url)

                if req.status_code == 200:

                    if 'myworkdayjobs' in job_url:
                        try:
                            job_json = json.loads(req.text)
                            if job_json['openGraphAttributes']['title']:
                                results = myworkdayjobs.Scraper().scrape(req.text, self.__keywords_dict)
                            else:
                                results['success'] = False
                                results['error_message'] = f'Error: The job is no longer available.'

                        except Exception as e:
                            pass
                else:
                    results['success'] = False
                    results['error_message'] = f'Error: The job is no longer available.'

                    # error job url
                    self.__logger.error(f"Status Code Error: {req.status_code}; Url: {req.url}")
                
                #self.__result_list.append(results)

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
                    results['error_message'] = f'Error: The job is no longer available.'

                #self.__result_list.append(results)

            else:
                results['success'] = False
                self.__logger.error(f"Wrong URL; Url: {job_url}")

            self.__logger.info(f"Job {count + 1} - \"{job_url}\": Scraping finished")

            self.__result_list.append(results)
        except Exception as e:
            self.__logger.error(f"Job {count + 1} - {job_url}; Error found; {e}")
