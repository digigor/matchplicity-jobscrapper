# -*- coding: UTF-8 -*-

import os
import re
import logging
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Tools:
    """
        This class contains some extra functions
    """

    @staticmethod
    def get_logger():
        """
            Create a Logging object
        """
        try:
            logger = logging.getLogger('output')
            if not logger.hasHandlers():
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

                file_handler = logging.FileHandler(os.path.join(os.path.abspath('.'), 'output.log'), mode='a+')
                file_handler.setFormatter(formatter)

                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)

                logger.setLevel(logging.INFO)
                logger.addHandler(file_handler)
                logger.addHandler(stream_handler)

            return logger
        except Exception as e:
            raise e

    @staticmethod
    def create_session(retries=RETRY_TIMES,
                       backoff_factor=0.3,
                       status_forcelist=(500, 502, 504)
                       ):
        try:
            session = requests.Session()
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            if HEADERS:
                session.headers.update(HEADERS)
            if PROXYSOCKET:
                session.proxies = ({
                    'http': f'http://{PROXYSOCKET}',
                    'https': f'http://{PROXYSOCKET}',
                })
            return session
        except Exception as e:
            raise e

    @staticmethod
    def create_driver():
        """
            Init driver with firefox
        :return: driver
        """
        try:
            options = Options()
            options.headless = PARAMETERS['headless']

            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            if PROXYSOCKET:
                desired_capability['proxy'] = {
                    "proxyType": "manual",
                    "httpProxy": PROXYSOCKET
                }
            driver = webdriver.Firefox(executable_path= "./geckodriver", options=options, capabilities=desired_capability)

            driver.maximize_window()
            return driver
        except Exception as e:
            raise e

    @staticmethod
    def search_keyword(keyword_list, string_text):
        """
             Search a keyword in a string
        :param keyword_list: list of keywords
        :param string_text: text no analyze
        :return: values
        """
        try:
            values_list = []
            for keyword in keyword_list:
                if re.search(fr"\b{keyword}\.?\b", string_text, re.IGNORECASE):
                    values_list.append(keyword)

            if values_list:
                return values_list
            else:
                return None
        except Exception as e:
            raise e
