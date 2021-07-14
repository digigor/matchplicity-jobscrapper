# -*- coding: UTF-8 -*-

import re
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from anticaptchaofficial.recaptchav2proxyless import *
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from constants import *


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

                fileHandler = logging.FileHandler('output.log', mode='a+')
                fileHandler.setFormatter(formatter)

                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(formatter)

                logger.setLevel(logging.INFO)
                logger.addHandler(fileHandler)
                logger.addHandler(streamHandler)

            return logger
        except Exception as e:
            raise e

    def create_driver(self):
        """
            Init driver with firefox
        :return: driver
        """
        try:
            options = Options()
            options.headless = PARAMETERS['headless']

            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            proxy = self.get_proxy()
            desired_capability['proxy'] = {
                "proxyType": "manual",
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy
            }
            driver = webdriver.Firefox(options=options, capabilities=desired_capability)

            driver.maximize_window()
            return driver
        except Exception as e:
            raise e

    def get_proxy(self):
        """
            Get a proxy
        :return: proxy
        """
        if PARAMETERS['proxyType'] == "proxyflow":
            try:
                tries = 0
                while tries < RETRY_TIMES:
                    result = requests.get(PROXYFLOW_URL)
                    if result.status_code == 200 and result.content:
                        proxy = (json.loads(result.content))['url']
                        proxy = re.findall(r'(?:https?://)(.*)', proxy)[0]

                        return proxy
                    else:
                        tries += 1

                raise Exception("No proxy found")
            except Exception as e:
                raise e
        elif PARAMETERS['proxyType'] == "stormproxies":
            return PARAMETERS['proxySocket']

    def retry_session(self,
                      retries=RETRY_TIMES,
                      backoff_factor=0.3,
                      status_forcelist=(500, 502, 504),
                      session=None,
                      proxy=None,
                      headers=None
                      ):
        session = session or requests.Session()
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
        if headers:
            session.headers.update(headers)
        proxy = self.get_proxy()
        session.proxies = ({
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        })
        return session

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

    @staticmethod
    def clean_number(number):
        # Cleaning first non numeric characters
        number = re.findall(re.compile(r'[0-9].*', re.DOTALL), number)
        if number:
            # Replace all ',' for '.' and replace 'o' for '0', and remove white spaces
            number = str(number).replace(',', '.').replace('o', '0').replace(' ', '')
            # Find all completed numbers whit dots and group in a list of elements
            number = re.findall(re.compile(r'([0-9.]+)', re.DOTALL), number)
            if number:
                # Remove extra dots and final dots
                number = re.sub(re.compile(r'\.(?!\w)', re.DOTALL), '', number[0])
                # Remove all dots except possible final decimal dots
                number = re.sub(re.compile(r'[^0-9.]|\.(?=.*\.)', re.DOTALL), '', number)
                # Finally remove the remain dot if not a decimal dot
                number = re.sub(re.compile(r'\.(?=[0-9]{3,})', re.DOTALL), '', number)

            return number

    @staticmethod
    def get_recaptcha_token(site_key, url):
        try:
            tries = 0
            while tries < 10:
                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key(ANTICAPTCHA_KEY)
                solver.set_website_url(url)
                solver.set_website_key(site_key)
                # make request to anticaptcha api
                g_recaptcha_response = solver.solve_and_return_solution()
                if g_recaptcha_response:
                    return g_recaptcha_response
                else:
                    tries += 1

            return None
        except Exception as e:
            raise e
