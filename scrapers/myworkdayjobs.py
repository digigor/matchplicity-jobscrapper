# -*- coding: UTF-8 -*-

import re
from dependencies import tools


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        self.__regex_dict = {
            'Years of Experience':
                re.compile(r'(?:\s)(\d)(?: ?\+?-? (?:or more )?years.*?experience)', re.IGNORECASE),
            'Salary':
                re.compile(r'(?:salary.*?)(\$[\d.,]+ to \$[\d.,]+)(?:\.?)', re.IGNORECASE),
            'GPA':
                re.compile(r'(?:(?:minimum|minimum GPA|overall.*?GPA) (?:of )?)(\d\.\d{1,2})(?: degree| cumulative GPA)?', re.IGNORECASE),
            'Virtual environment':
                re.compile(r'(virtual job|virtual.*?team|virtual remote|work at home|work-at-home|home office|remote work|virtual option|home based)', re.IGNORECASE),
            'Physical environment':
                re.compile(r'(physical office|physical environment|office based)', re.IGNORECASE),
            'Hybrid environment':
                re.compile(r'(hybrid environment|work at home/office|office and home|hybrid/work at home)', re.IGNORECASE)
        }
        self.__values_dict = {
            'Job Title': '',
            'Job Description': '',
            'Job Application URL': '',
            'Job Type': '',
            'Job Location': '',
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

            # self.__values_dict['Job Application URL'] = job_json['openGraphAttributes']['url'] + '/apply'
            self.__values_dict['Job Application URL'] = job_json['openGraphAttributes']['url']

            for element in job_json['body']['children'][1]['children'][1]['children']:
                try:
                    if element['iconName'] == "JOB_TYPE":
                        self.__values_dict['Job Type'] = element['imageLabel']
                        break
                except:
                    pass

            aux = []
            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['iconName'] == "LOCATION":
                        aux.append(element['imageLabel'])
                except:
                    pass
            if aux:
                self.__values_dict['Job Location'] = aux

            years_list = self.__regex_dict['Years of Experience'].findall(job_json['openGraphAttributes']['description'])
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

            aux = self.__regex_dict['Salary'].findall(job_json['openGraphAttributes']['description'])
            if aux:
                self.__values_dict['Salary'] = aux[0]

            self.__values_dict['Preferred Previous Job Titles'] = self.__tools_obj.search_keyword(
                keywords_dict['Titles'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Soft Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Soft Skills'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Technical Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Technical Skills'], job_json['openGraphAttributes']['description'])

            self.__values_dict['Preferred Majors'] = self.__tools_obj.search_keyword(
                keywords_dict['Majors'], job_json['openGraphAttributes']['description'])

            aux = self.__regex_dict['GPA'].findall(job_json['openGraphAttributes']['description'])
            if aux:
                self.__values_dict['Min GPA requirement'] = aux[0]

            if self.__regex_dict['Hybrid environment'].search(job_json['openGraphAttributes']['description']):
                self.__values_dict['Work environment'] = "Hybrid"
            elif self.__regex_dict['Virtual environment'].search(job_json['openGraphAttributes']['description']):
                if self.__regex_dict['Physical environment'].search(job_json['openGraphAttributes']['description']):
                    self.__values_dict['Work environment'] = "Hybrid"
                else:
                    self.__values_dict['Work environment'] = "Virtual"
            elif self.__regex_dict['Physical environment'].search(job_json['openGraphAttributes']['description']):
                self.__values_dict['Work environment'] = "Physical"

            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
