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
            # Title
            for xpath in self.__xpath_dict['title']:
                result = driver.find_elements_by_xpath(xpath)
                if result:
                    self.__values_dict['Job Title'] = result[0].text
                    break

            # Description
            for xpath in self.__xpath_dict['description']:
                result = driver.find_elements_by_xpath(xpath)
                if result:
                    # save the HTML tags
                    self.__values_dict['Job Description'] = (result[0]).get_attribute('innerHTML')
                    break

            # Application URL
            self.__values_dict['Job Application URL'] = job_url

            # job types
            for xpath in self.__xpath_dict['job_type']:
                result = driver.find_elements_by_xpath(xpath)
                if result:

                    aux = self.__data_cleaning.MatcherParser(result[0].text)

                    if 'experienced' in self.__data_cleaning.MatcherParser(result[0].text):
                        self.__values_dict['Job Type'] = "Full Time"
                    else:
                        self.__values_dict['Job Type'] = result[0].text
                    break

            # job location
            for xpath in self.__xpath_dict['job_location']:
                result = driver.find_elements_by_xpath(xpath)
                if result:
                    # save the HTML tags
                    self.__values_dict['Job Location'] = result[0].text
                    break

            # years of experience
            years_list = self.__regex_dict['Years of Experience'].findall(driver.page_source)
            aux = ''
            for year in years_list:
                if not aux:
                    aux = int(year)
                else:
                    if int(year) < aux:
                        aux = int(year)

            self.__values_dict['Preferred Years of Experience'] = aux

            # Previous job titles
            self.__values_dict['Preferred Previous Job Titles'] = self.__tools_obj.search_keyword(
                keywords_dict['Titles'], driver.page_source)

            # Salary
            result = self.__regex_dict['Salary'].findall(driver.page_source)
            if result:
                self.__values_dict['Salary'] = result[0]

            # Preferred Certifications
            self.__values_dict['Preferred Certifications'] = self.__tools_obj.search_keyword(
                keywords_dict['Certifications'], driver.page_source)

            # Soft Skills
            self.__values_dict['Soft Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Soft Skills'], driver.page_source)

            # Technical Skills
            self.__values_dict['Technical Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Technical Skills'], driver.page_source)

            # Preferred Majors
            self.__values_dict['Preferred Majors'] = self.__tools_obj.search_keyword(
                keywords_dict['Majors'], driver.page_source)

            # Salary
            result = self.__regex_dict['GPA'].findall(driver.page_source)
            if result:
                self.__values_dict['Min GPA requirement'] = result[0]

            # Work environment
            if self.__regex_dict['Hybrid environment'].search(driver.page_source):
                self.__values_dict['Work environment'] = "Hybrid"
            elif self.__regex_dict['Virtual environment'].search(driver.page_source):
                if self.__regex_dict['Physical environment'].search(driver.page_source):
                    self.__values_dict['Work environment'] = "Hybrid"
                else:
                    self.__values_dict['Work environment'] = "Virtual"
            elif self.__regex_dict['Physical environment'].search(driver.page_source):
                self.__values_dict['Work environment'] = "Physical"



            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
