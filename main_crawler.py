# -*- coding: UTF-8 -*-

import json
import re
import requests
from dependencies import tools
from config import *
import crawler


class MainCrawler:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()

    def crawl(self):
        try:
            self.__logger.info("Starting execution...")

            # create session
            session = self.__tools_obj.create_session()

            # iterate over urls
            for main_url in URLS:
                try:
                    self.__logger.info(f"Searching: {main_url}")

                    job_urls = set()
                    index = 50
                    next_url = None

                    # make requests
                    req = session.get(main_url)
                    while True:
                        if req.status_code == 200:
                            # load response json
                            main_json = json.loads(req.text)

                            # iterate over json
                            for element in main_json['body']['children'][0]['children'][0]['listItems']:
                                try:
                                    job_url = element['title']['commandLink']
                                    job_url = main_url + re.findall(r'(/job/.*)', job_url)[0]
                                    job_urls.add(job_url)
                                except Exception as e:
                                    self.__logger.error(f"Url: {req.url}; Error found; {e}")

                            if not next_url:
                                # get next page
                                next_url = main_json['body']['children'][0]['endPoints'][1]['uri']
                                next_url = main_url + re.findall(r'(/fs/.*)', next_url)[0]

                            # make requests
                            req = session.get(f"{next_url}/{index}")
                            index += 50
                        else:
                            break

                    crawler_obj = crawler.Crawler()
                    crawler_obj.run(job_urls)
                except Exception as e:
                    self.__logger.error(f"{main_url}: Error found; {e}")

            # execution finished
            self.__logger.info("Finishing execution...")
        except Exception as e:
            self.__logger.error(f"::Main Crawler:: Error found; {e}")


if __name__ == '__main__':
    MainCrawler().crawl()
