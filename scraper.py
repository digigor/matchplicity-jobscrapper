# -*- coding: UTF-8 -*-
import re

from dependencies import tools


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        self.__regex_dict = {
            'Preferred Years of Experience': re.compile(r'([\d]+)(?=\+?-? (?:or more )?years.*?experience)', re.IGNORECASE)
        }
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

    def scrape(self, job_json, keywords_dict):
        try:
            self.__values_dict['Job Title'] = job_json['openGraphAttributes']['title']

            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['ecid'].__contains__("jobDescription"):
                        self.__values_dict['Job Description'] = element['text']
                        break
                except:
                    pass

            self.__values_dict['Job Application URL'] = job_json['openGraphAttributes']['url'] + '/apply'

            for element in job_json['body']['children'][1]['children'][1]['children']:
                try:
                    if element['iconName'] == "JOB_TYPE":
                        self.__values_dict['Job Type'] = element['imageLabel']
                        break
                except:
                    pass

            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['iconName'] == "LOCATION":
                        self.__values_dict['Job Location'].append(element['imageLabel'])
                except:
                    pass

            years_list = self.__regex_dict['Preferred Years of Experience'].findall(job_json['openGraphAttributes']['description'])
            aux = ''
            for year in years_list:
                if not aux:
                    aux = int(year)
                else:
                    if int(year) < aux:
                        aux = int(year)
            self.__values_dict['Preferred Years of Experience'] = aux

            self.__values_dict['Preferred Certifications'] = self.__tools_obj.search_keyword(
                keywords_dict['Certifications'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Preferred Previous Job Titles'] = self.__tools_obj.search_keyword(
                keywords_dict['Titles'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Soft Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Soft Skills'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Technical Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Technical Skills'], job_json['openGraphAttributes']['description'])

            if re.search(r'internship', job_json['openGraphAttributes']['description'], re.IGNORECASE):
                self.__values_dict['Preferred Majors'] = "Internship"

            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
