# -*- coding: UTF-8 -*-

import re
from dependencies import tools, data_cleaning


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__data_cleaning = data_cleaning.DataCleaner()
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


        self.__xpath_dict = {
            "title": ['//*[@id="requisitionDescriptionInterface.reqTitleLinkAction.row1"]'],
            "description": ['//*[@id="requisitionDescriptionInterface.ID1722.row1"]',
                            '//*[@id="requisitionDescriptionInterface.ID2011.row1"]',
                            '//*[@id="requisitionDescriptionInterface.ID1531.row1"]'],
            "job_type": ['//*[@id="requisitionDescriptionInterface.ID1808.row1"]',
                          '//*[@id="requisitionDescriptionInterface.ID1912.row1"]',
                          '//*[@id="requisitionDescriptionInterface.ID1603.row1"]'],
            "job_location": ['//*[@id="requisitionDescriptionInterface.ID1724.row1"]',
                             '//*[@id="requisitionDescriptionInterface.ID1714.row1"]',
                             '//*[@id="requisitionDescriptionInterface.ID1657.row1"]']
        }



    def scrape(self, driver, keywords_dict, job_url):
        try:
            if not re.search(r'The job is no longer available', driver.page_source):

                # Title
                for xpath in self.__xpath_dict['title']:
                    result = driver.find_elements_by_xpath(xpath)
                    if result:
                        self.__values_dict['title'] = result[0].text
                        break

                # Description
                for xpath in self.__xpath_dict['description']:
                    result = driver.find_elements_by_xpath(xpath)
                    if result:
                        # save the HTML tags
                        self.__values_dict['description'] = (result[0]).get_attribute('innerHTML')
                        break

                # Application URL
                self.__values_dict['application_url'] = job_url

                # job types
                for xpath in self.__xpath_dict['job_type']:
                    result = driver.find_elements_by_xpath(xpath)
                    if result:

                        aux = self.__data_cleaning.MatcherParser(result[0].text)

                        if 'experienced' in self.__data_cleaning.MatcherParser(result[0].text):
                            self.__values_dict['job_type'].append("Full Time")
                        else:
                            self.__values_dict['job_type'].append(result[0].text)
                        break

                # job location
                for xpath in self.__xpath_dict['job_location']:
                    result = driver.find_elements_by_xpath(xpath)
                    if result:
                        # save the HTML tags
                        self.__values_dict['job_locations'].append(result[0].text)
                        break

                # years of experience
                years_list = self.__regex_dict['Years of Experience'].findall(driver.page_source)

                if not years_list:
                    if re.search('years', self.__values_dict['title']):
                        years_list = re.findall(r'([0-9]+)', self.__values_dict['title'])

                if years_list:
                    self.__values_dict['preferred_years_experience'] = years_list

                # Previous job titles
                if self.__tools_obj.search_keyword(
                    keywords_dict['Titles'], driver.page_source):

                    self.__values_dict['preferred_years_experience'] = self.__tools_obj.search_keyword(
                        keywords_dict['Titles'], driver.page_source)

                # Salary
                result = self.__regex_dict['Salary'].findall(driver.page_source)
                if result:
                    try:
                        self.__values_dict['salary'] = int(result[0])
                    except Exception as e:
                        pass

                # Preferred Certifications
                if self.__tools_obj.search_keyword(
                    keywords_dict['Certifications'], driver.page_source):
                    self.__values_dict['preferred_certification'] = self.__tools_obj.search_keyword(
                        keywords_dict['Certifications'], driver.page_source)

                # Soft Skills
                if self.__tools_obj.search_keyword(
                    keywords_dict['Soft Skills'], driver.page_source):
                    self.__values_dict['preferred_soft_skill'] = self.__tools_obj.search_keyword(
                        keywords_dict['Soft Skills'], driver.page_source)

                # Technical Skills
                if self.__tools_obj.search_keyword(
                    keywords_dict['Technical Skills'], driver.page_source):
                    self.__values_dict['preferred_technical_skill'] = self.__tools_obj.search_keyword(
                        keywords_dict['Technical Skills'], driver.page_source)

                # Preferred Majors
                if self.__tools_obj.search_keyword(
                    keywords_dict['Majors'], driver.page_source):
                    self.__values_dict['job_preferred_major'] = self.__tools_obj.search_keyword(
                        keywords_dict['Majors'], driver.page_source)

                # Salary
                result = self.__regex_dict['GPA'].findall(driver.page_source)
                if result:
                    try:
                        self.__values_dict['job_gpa'] = int(result[0])
                    except Exception as e:
                        pass

            else:
                self.__values_dict['description'] = 'the job is no longer available'


            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
