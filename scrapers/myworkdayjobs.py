# -*- coding: UTF-8 -*-

import re
import json
from dependencies import tools, data_cleaning, usa_states


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
                re.compile(r'(hybrid environment|work at home/office|office and home|hybrid/work at home)', re.IGNORECASE),
            'internship': ['internship', 'Internship']
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
            'success': None,
            'error_message': None,
            'source': 'myworkdayjobs'
            #"'Work environment': '',
            #'is_nation_wid': None
        }

    def scrape(self, job_url, session, keywords_dict):

        """def abreviation(self, countr, stat):

            if countr == "USA":
                countr = "United States of America"
                for sta, ab in usa_states.us_state_to_abbrev.items():
                    if ab == stat:
                    stat = sta

            return countr, stat"""

        try:
            req = session.get(job_url)
            job_json = json.loads(req.text)

            # title
            if job_json['openGraphAttributes']['title']:
                self.__values_dict['title'] = job_json['openGraphAttributes']['title']

            # description
            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['ecid'].__contains__("jobDescription"):
                        self.__values_dict['description'] = element['text']
                        break
                except Exception as e:
                    pass

            # aplication url
            self.__values_dict['application_url'] = job_json['openGraphAttributes']['url']

            #job_type
            for element in job_json['body']['children'][1]['children'][1]['children']:
                try:
                    if element['iconName'] == "JOB_TYPE":

                        jobtype = self.__data_cleaning.MatcherParser(element['imageLabel'])

                        if jobtype == 'fulltime':

                            if self.__tools_obj.search_keyword(self.__regex_dict['internship'], job_json['openGraphAttributes']['description']):
                                self.__values_dict['job_type'].append('full-time-int')
                            else:
                                self.__values_dict['job_type'].append('full-time')

                        elif jobtype == 'parttime':

                            if  self.__tools_obj.search_keyword(self.__regex_dict['internship'], job_json['openGraphAttributes']['description']):
                                self.__values_dict['job_type'].append('part-time-int')
                            else:
                                self.__values_dict['job_type'].append('part-time')

                except:
                    pass

            #location
            aux = []
            for element in job_json['body']['children'][1]['children'][0]['children']:
                try:
                    if element['iconName'] == "LOCATION":
                        aux.append(element['imageLabel'])
                except:
                    pass
            if aux:

                try:
                    if "-" in aux[0]:
                        location = aux[0].split("-")
                    elif "," in aux[0]:
                        location = aux[0].split(",")
                    else:
                        location = aux
                    location_dict = {
                        "country": None,
                        "state": None,
                        "city": None
                    }

                    if len(location) == 1:
                        location_dict['country'] = location[0].lstrip(' ').rstrip(' ')

                    elif len(location) == 2:
                        aux = location[1].lstrip(' ').rstrip(' ')
                        country = location[0].lstrip(' ').rstrip(' ')
                        if country == "USA":
                           country = "United States"
                           for sta , abrev in usa_states.us_state_to_abbrev.items():
                                if abrev == aux:
                                    aux = sta

                        for loc in keywords_dict['locations']:
                            if country in country in loc['country']:
                                if aux in loc['state']:
                                    dict_aux = {'country': country,
                                                'state': aux,
                                                'city': loc['city']}

                                elif aux in loc['city']:
                                    dict_aux = {'country': country,
                                                'state': loc['state'],
                                                'city': aux}
                                else:
                                    dict_aux = {'country': country,
                                                'state': None,
                                                'city': aux}

                        location_dict['country'] = dict_aux['country']
                        location_dict['state'] = dict_aux['state']
                        location_dict['city'] = dict_aux['city']

                    elif len(location) == 3:
                        city = location[-1].lstrip(' ').rstrip(' ')
                        state = location[-2].lstrip(' ').rstrip(' ')
                        country = location[-3].lstrip(' ').rstrip(' ')
                        if country == "USA":
                            country = "United States"
                            for sta, abrev in usa_states.us_state_to_abbrev.items():
                                if abrev == state:
                                    state = sta

                        # try:
                        #     dict_aux = next(item for item in keywords_dict['locations'] if item['country'] in country and item['city'] in city and item['state'] in state)
                        #     location_dict['country'] = dict_aux['country']
                        #     location_dict['state'] = dict_aux['state']
                        #     location_dict['city'] = dict_aux['city']
                        # except Exception as e:
                        #     location_dict['country'] = country
                        #     location_dict['state'] = state
                        #     location_dict['city'] = city
                        for loc in keywords_dict['locations']:
                            if country in loc['country'] and state in loc['state'] and city in loc['city']:
                                location_dict['country'] = loc['country']
                                location_dict['state'] = loc['state']
                                location_dict['city'] = loc['city']
                            elif country in loc['country'] and state in loc['state']:
                                location_dict['country'] = country
                                location_dict['state'] = state
                                location_dict['city'] = city
                            elif country in loc['country'] and city in loc['city']:
                                location_dict['country'] = country
                                location_dict['state'] = loc['state']
                                location_dict['city'] = city

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

            if self.__tools_obj.search_keyword(keywords_dict['Titles'], job_json['openGraphAttributes']['description']):
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

            self.__values_dict['success'] = True

        except Exception as e:

            self.__values_dict['success'] = False
            self.__logger.error(f"::Scraper:: Error found; {e}")

        return self.__values_dict



