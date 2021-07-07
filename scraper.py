# -*- coding: UTF-8 -*-
import re

from dependencies import tools


class Scraper:

    def __init__(self):
        self.__tools_obj = tools.Tools()
        self.__logger = self.__tools_obj.get_logger()
        self.__regex_dict = {
            'Job Title': re.compile(r'', re.IGNORECASE),
            'Job Description': re.compile(r'', re.IGNORECASE),
            'Job Type': re.compile(r'', re.IGNORECASE),
            'Job Location': re.compile(r'', re.IGNORECASE),
            'Preferred Years of Experience': re.compile(r'', re.IGNORECASE),
            'Preferred Previous Job Titles': re.compile(r'', re.IGNORECASE),
            'Salary': re.compile(r'', re.IGNORECASE),
            'Preferred Certifications': re.compile(r'', re.IGNORECASE),
            'Soft Skills': re.compile(r'', re.IGNORECASE),
            'Technical Skills': re.compile(r'', re.IGNORECASE),
            'Preferred Majors': re.compile(r'', re.IGNORECASE),
            'Min GPA requirement': re.compile(r'', re.IGNORECASE),
            'Work environment': re.compile(r'', re.IGNORECASE)
        }

    def scrape(self, job_html, job_url):
        try:
            values_dict = {}
            for key, value in self.__regex_dict.items():
                aux = None
                for regex in value:
                    try:
                        aux = regex.findall(job_html)[0]
                        break
                    except:
                        pass

                values_dict[key] = aux

            values_dict['Job Application URL'] = job_url
            return values_dict
        except Exception as e:
            self.__logger.error(f"::Scraper:: Error found; {e}")
            raise
