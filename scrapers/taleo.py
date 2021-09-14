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
            'source': 'taleo'
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
                try:
                    for xpath in self.__xpath_dict['title']:
                        result = driver.find_elements_by_xpath(xpath)
                        if result:
                            self.__values_dict['title'] = result[0].text
                            break
                except Exception as e:
                    pass

                # Description
                try:
                    for xpath in self.__xpath_dict['description']:
                        result = driver.find_elements_by_xpath(xpath)
                        if result:
                            # save the HTML tags
                            self.__values_dict['description'] = (result[0]).get_attribute('innerHTML')
                            break
                except Exception as e:
                    pass
                # Application URL
                self.__values_dict['application_url'] = job_url

                # job types
                for xpath in self.__xpath_dict['job_type']:
                    
                    try:
                        if driver.find_elements_by_xpath(xpath):
                            results = driver.find_elements_by_xpath(xpath)
                            job_to_compare = self.__data_cleaning.MatcherParser(results[0].text)


                            if job_to_compare == 'fulltime':

                                if  self.__tools_obj.search_keyword(self.__regex_dict['internship'], self.__values_dict['description']):
                                    self.__values_dict['job_type'].append('full-time-int')
                                else:
                                    self.__values_dict['job_type'].append('full-time')

                            elif job_to_compare == 'parttime':
                                
                                if  self.__tools_obj.search_keyword(self.__regex_dict['internship'], self.__values_dict['description']):
                                    self.__values_dict['job_type'].append('part-time-int')
                                else:
                                    self.__values_dict['job_type'].append('part-time')
                            
                            elif job_to_compare == 'intern':
                                self.__values_dict['job_type'].append('full-time-int')
                            
                            elif job_to_comapre =='experienced':
                                self.__values_dict['job_type'].append('full-time')

                            break  
                    except Exception as e:
                        pass
                # job location
                for xpath in self.__xpath_dict['job_location']:
                    try:
                        result = driver.find_elements_by_xpath(xpath)
                        if result:
                            element = (driver.find_elements_by_xpath(xpath)[0].text)                        
                            element = element.replace("Non-Japan Asia-","").replace("Americas", "").replace("Europe, Middle East, Africa", "")
                            location_list = element.split("-")
                            location_dict = {
                                "country": None,
                                "state": None,
                                "city": None
                            }
                            if len(location_list) == 1:
                                location_dict['country'] = location_list[0].lstrip(' ').rstrip(' ')

                            elif len(location_list) == 2:
                                aux = location_list[-1].lstrip(' ').rstrip(' ')
                                country =location_list[-2].lstrip(' ').rstrip(' ')
                                dict_aux = next(item for item in keywords_dict['locations'] if item['country'] in country and (item['city'] in aux or item['state'] in aux))
                                location_dict['country'] = dict_aux['country']
                                location_dict['state'] =  dict_aux['state']
                                location_dict['city'] =  dict_aux['city']
                                #location_dict['country'] = location_list[-2].lstrip(' ').rstrip(' ')
                                #location_dict['state'] = location_list[-1].lstrip(' ').rstrip(' ')

                            elif len(location_list)>=3:
                                city =  location_list[-1].lstrip(' ').rstrip(' ')
                                state = location_list[-2].lstrip(' ').rstrip(' ')
                                country = location_list[-3].lstrip(' ').rstrip(' ')
                                dict_aux = next(item for item in keywords_dict['locations'] if item['country'] in country and item['city'] in city and item['state'] in state)
                                location_dict['country'] = dict_aux['country']
                                location_dict['state'] =  dict_aux['state']
                                location_dict['city'] =  dict_aux['city']
                         

                            self.__values_dict['job_locations'].append(location_dict)
                    except Exception as e:
                        pass
                      

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

                    self.__values_dict['preferred_previous_job_title'] = self.__tools_obj.search_keyword(
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
                
                self.__values_dict['success'] = True

            else:
                self.__values_dict['success'] = False

          
        except Exception as e:
            self.__values_dict['success'] = False

            self.__logger.error(f"::Scraper:: Error found; {e}")

        
        return self.__values_dict