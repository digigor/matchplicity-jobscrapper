# -*- coding: UTF-8 -*-
import re

from dependencies import tools


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        self.__values_dict = {
            'Job Title': '',
            'Job Description': '',
            'Job Application URL': '',
            'Job Type': '',
            'Job Location': [],
            'Preferred Years of Experience': '',
            'Preferred Previous Job Titles': '',
            'Salary': '',
            'Preferred Certifications': '',
            'Soft Skills': '',
            'Technical Skills': '',
            'Preferred Majors': '',
            'Min GPA requirement': '',
            'Work environment': ''
        }

    def scrape(self, job_json):
        try:
            self.__values_dict['Job Title'] = job_json['openGraphAttributes']['title']
            self.__values_dict['Job Description'] = job_json['openGraphAttributes']['description']
            self.__values_dict['Job Application URL'] = job_json['openGraphAttributes']['url']

            for element in job_json['body']['children'][1]['children'][1]['children']:
                try:
                    if element['iconName'] == "JOB_TYPE":
                        self.__values_dict['Job Type'].append(element['imageLabel'])
                        break
                except:
                    pass

            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['iconName'] == "LOCATION":
                        self.__values_dict['Job Location'].append(element['imageLabel'])
                except:
                    pass

            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
