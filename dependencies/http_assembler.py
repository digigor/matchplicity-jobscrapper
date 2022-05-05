# -*- coding: UTF-8 -*-

import requests
import time
import random
from aslibs.tools import log

#Todo falta testear, esta no es la ultima version. tenemos una que maneja session instead
class HTTPAssembler:

    def __init__(self):
        self.__logger = log.Log().get_logger()


    @staticmethod
    def create_session(retries=5,
                       backoff_factor=0.3,
                       status_forcelist=(500, 502, 504),
                       headers=None,
                       proxy=None
                       ):
        """
            Create a requests session
        :param retries:
        :param backoff_factor:
        :param status_forcelist:
        :param headers:
        :param proxy:
        :return: session
        """
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
            if headers:
                session.headers.update(headers)
            if proxy:
                session.proxies = ({
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}',
                })

            return session
        except Exception as e:
            raise e


    def post_requests(self, URL, body, Headers= None,stream=None, proxydict=None):
        '''
            Este metodo se encarga de realizar un POST Requests y asegurarse que tire status 200
        :param URL: POST URL
        :param Headers: diccionario de headers
        :param ParamDict: diccionario de datos para el parametro del POST
        :return: PostResponse y contenido si status es 200, de lo contrario False
        '''
        tries = 0
        ban = 0
        try:
            while ban == 0:
                # proxydict = {'http': 'http://127.0.0.1:8888/'}

                try:
                    if stream == True:
                        if proxydict:
                            post_response = requests.post(URL, data=body, headers=Headers, stream=True, proxies=proxydict)
                        else:
                            post_response = requests.post(URL, data=body, headers=Headers, stream=True)
                    else:
                        if proxydict:
                            post_response = requests.post(URL, data=body, headers=Headers, proxies=proxydict)
                        else:
                            post_response = requests.post(url=URL, data=body, headers=Headers)

                    if post_response.status_code == 200:
                        b = 1
                        return post_response
                    else:
                        raise
                except Exception as e:
                    self.__logger.error(f'Error found, trying again: {tries}/{5}; Error: {e}; URL: {URL}')
                    time.sleep((random.randint(1, 3)))
                    ban = 0
                    tries += 1

                if tries == 5:
                    self.__logger.error('Maximum tries reached')
                    raise
        except Exception as e:
            self.__logger.error(f'Error found on http_assembler::post_request; error: {e}')
            raise


    def get_request(self, URL, Headers=None, stream=None, proxydict = None):
        '''
            Este metodo se encarga de realizar un GET Requests y asegurarse que tire status 200
        :param URL: URL del GET requests
        :param Headers: Diccionario de Headers
        :return: GetResponse y contenido si status es 200, de lo contrario False
        '''

        tries = 0
        ban = 0
        try:
            while ban == 0:

                try:
                    if stream == True:
                        if proxydict:
                            get_response = requests.get(URL, headers=Headers, stream=True, proxies=proxydict)
                        else:
                            get_response = requests.get(URL, headers=Headers, stream=True)
                    else:
                        if proxydict:
                            get_response = requests.get(URL, headers=Headers, proxies=proxydict)
                        else:
                            get_response = requests.get(url=URL, headers=Headers)

                    if get_response.status_code == 200:
                        b = 1
                        return get_response
                    else:
                        raise
                except Exception as e:
                    self.__logger.error(f'Error found, trying again: {tries}/{5}; Error: {e}; URL: {URL}')
                    time.sleep((random.randint(1, 3)))
                    ban = 0
                    tries += 1

                if tries == 5:
                    self.__logger.error('Maximum tries reached')
                    raise
        except Exception as e:
            self.__logger.error(f'Error found on http_assembler::get_request; error: {e}')
            raise
