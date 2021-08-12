# -*- coding: UTF-8 -*-

import re
from lxml import html
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

        self.__xpath_dict = {
            "title":['//span[@class="titlepage" and contains(@id, "Title")]/text()'],
            "description":['//div[@class="contentlinepanel" and contains(@id, "requisitionDescriptionInterface.ID2011.row1")]//text()'],
            "full_type" : ['//span[@id="requisitionDescriptionInterface.ID1912.row1" ]/text()'],
            "location" : ['//span[@id="requisitionDescriptionInterface.ID1714.row1" ]/text()']
        }

    def find_element(self, key, tree, concat = False):
        for xpth in self.__xpath_dict[key]:
            result = tree.xpath(xpth)
            if result:
                if concat:
                    return ' '.join(result)
                return result[0]
        return ''
    
    

    def scrape(self, job_html, keywords_dict):
        try:

            #TODO pide el html entero de cada texto

            tree = html.document_fromstring(job_html)

            self.__values_dict['Job Title'] = tree.xpath('//span[@class="titlepage" and contains(@id, "Title")]/text()')  # self.find_element("title", tree)

            self.__values_dict['Job Description'] = self.find_element("description", tree, concat=True)

            self.__values_dict['Job Application URL'] = '' #TODO ver que poner aqui, pide login

            self.__values_dict['Job Type'] = self.find_element("full_type", tree)

            self.__values_dict['Job Location'] = self.find_element("location", tree)

            years_list = self.__regex_dict['Years of Experience'].findall(self.__values_dict['Job Description'] )
            aux = ''
            for year in years_list:
                if not aux:
                    aux = int(year)
                else:
                    if int(year) < aux:
                        aux = int(year)
            self.__values_dict['Preferred Years of Experience'] = aux

            self.__values_dict['Preferred Certifications'] = self.__tools_obj.search_keyword(
                keywords_dict['Certifications'],self.__values_dict['Job Description'] )

            aux = self.__regex_dict['Salary'].findall(self.__values_dict['Job Description'] )
            if aux:
                self.__values_dict['Salary'] = aux[0]

            self.__values_dict['Preferred Previous Job Titles'] = self.__tools_obj.search_keyword(
                keywords_dict['Titles'], self.__values_dict['Job Description'])

            self.__values_dict['Soft Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Soft Skills'],self.__values_dict['Job Description'])

            self.__values_dict['Technical Skills'] = self.__tools_obj.search_keyword(
                keywords_dict['Technical Skills'], self.__values_dict['Job Description'])

            self.__values_dict['Preferred Majors'] = self.__tools_obj.search_keyword(
                keywords_dict['Majors'], self.__values_dict['Job Description'])

            aux = self.__regex_dict['GPA'].findall(self.__values_dict['Job Description'])
            if aux:
                self.__values_dict['Min GPA requirement'] = aux[0]

            if self.__regex_dict['Hybrid environment'].search(self.__values_dict['Job Description']):
                self.__values_dict['Work environment'] = "Hybrid"
            elif self.__regex_dict['Virtual environment'].search(self.__values_dict['Job Description']):
                if self.__regex_dict['Physical environment'].search(self.__values_dict['Job Description']):
                    self.__values_dict['Work environment'] = "Hybrid"
                else:
                    self.__values_dict['Work environment'] = "Virtual"
            elif self.__regex_dict['Physical environment'].search(self.__values_dict['Job Description']):
                self.__values_dict['Work environment'] = "Physical"

            return self.__values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
