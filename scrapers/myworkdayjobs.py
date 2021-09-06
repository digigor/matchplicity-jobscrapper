# -*- coding: UTF-8 -*-

import re
import json
from dependencies import tools, data_cleaning


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        self.__data_cleaning = data_cleaning.DataCleaner()
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
            'title': None,
            'description': None,
            'application_url': None,
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
            #"'Work environment': '',
            #'is_nation_wid': None
        }

    def scrape(self, req, keywords_dict):
        try:

            job_json = json.loads(req)
            if job_json['openGraphAttributes']['title']:
                self.__values_dict['title'] = job_json['openGraphAttributes']['title']

            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['ecid'].__contains__("jobDescription"):
                        self.__values_dict['description'] = element['text']
                        break
                except:
                    pass

            self.__values_dict['application_url'] = job_json['openGraphAttributes']['url']

            for element in job_json['body']['children'][1]['children'][1]['children']:
                try:
                    if element['iconName'] == "JOB_TYPE":
                        self.__values_dict['job_type'].append(element['imageLabel'])
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
                try:
                    location = aux[0].split("-")
                    location_dict = {
                        "country": None,
                        "state": None,
                        "city": None
                    }
                    if len(location) == 1:
                        location_dict['country'] = location[0].lstrip(' ').rstrip(' ')

                    elif len(location) == 2:
                        location_dict['country'] = location[0].lstrip(' ').rstrip(' ')
                        location_dict['state'] = location[1].lstrip(' ').rstrip(' ')

                    elif len(location) == 3:
                        location_dict['country'] = location[0].lstrip(' ').rstrip(' ')
                        location_dict['state'] = location[1].lstrip(' ').rstrip(' ')
                        location_dict['city'] = location[2].lstrip(' ').rstrip(' ')

                    self.__values_dict['job_locations'].append(location_dict)
                except Exception as e:
                    pass

            years_list = self.__regex_dict['Years of Experience'].findall(job_json['openGraphAttributes']['description'])
            aux = ''
            for year in years_list:
                if not aux:
                    aux = int(year)
                else:
                    if int(year) < aux:
                        aux = int(year)
            if aux:
                self.__values_dict['preferred_years_experience'].append(int(aux))

            self.__values_dict['preferred_certification'] = (self.__tools_obj.search_keyword(
                keywords_dict['Certifications'], job_json['openGraphAttributes']['description']))

            aux = self.__regex_dict['Salary'].findall(job_json['openGraphAttributes']['description'])
            if aux:
                try:
                    self.__values_dict['salary'] = aux[0]
                except Exception as e:
                    pass

            if self.__tools_obj.search_keyword(
                keywords_dict['Titles'], job_json['openGraphAttributes']['description']):
                self.__values_dict['preferred_previous_job_title'] = self.__tools_obj.search_keyword(
                    keywords_dict['Titles'], job_json['openGraphAttributes']['description'])

            if (self.__tools_obj.search_keyword(
                keywords_dict['Soft Skills'], job_json['openGraphAttributes']['description'])):

                self.__values_dict['preferred_soft_skill'] = (self.__tools_obj.search_keyword(
                    keywords_dict['Soft Skills'], job_json['openGraphAttributes']['description']))

            if self.__tools_obj.search_keyword(
                keywords_dict['Technical Skills'], job_json['openGraphAttributes']['description']):
                self.__values_dict['preferred_technical_skill'] = self.__tools_obj.search_keyword(
                    keywords_dict['Technical Skills'], job_json['openGraphAttributes']['description'])

            if self.__tools_obj.search_keyword(
                keywords_dict['Majors'], job_json['openGraphAttributes']['description']):
                self.__values_dict['job_preferred_major'] = self.__tools_obj.search_keyword(
                    keywords_dict['Majors'], job_json['openGraphAttributes']['description'])

            aux = self.__regex_dict['GPA'].findall(job_json['openGraphAttributes']['description'])
            if aux:
                try:
                    self.__values_dict['job_gpa'] = int(aux[0])
                except Exception as e:
                    pass


        except Exception as e:

            self.__values_dict['description'] = 'the job is no longer available'
            self.__logger.error(f"::Scraper:: Error found; {e}")

        return self.__values_dict

