import requests
import json
import re
from dependencies import tools, data_cleaning, usa_states


class Scraper:

  def __init__(self):
    self.__tools_obj = tools.Tools()
    self.__logger = self.__tools_obj.get_logger()
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
      # "'Work environment': '',
      # 'is_nation_wid': None
    }

  def scrape(self, job_url, keywords_dict):

    try:
      job = re.findall(r'(?:job/)(.*)', job_url)[0]

      url_final = f"https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/job/{job}"

      response = requests.request("GET", url_final)
      job_json = json.loads(response.text)

      # title
      if job_json['jobPostingInfo']['title']:
        self.__values_dict['title'] = job_json['jobPostingInfo']['title']

      # description
      if job_json['jobPostingInfo']['jobDescription']:
        self.__values_dict['description'] = job_json['jobPostingInfo']['jobDescription']

      # application_url
      self.__values_dict['application_url'] = job_url

      # job_type
      if job_json['jobPostingInfo']['timeType']:
        self.__values_dict['job_type'] = job_json['jobPostingInfo']['timeType']

      # location
      list_location = []
      if job_json['jobPostingInfo']['location']:
        list_location.append(job_json['jobPostingInfo']['location'])
        if job_json['jobPostingInfo']['additionalLocations']:
          for loc in job_json['jobPostingInfo']['additionalLocations']:
            list_location.append(loc)


      self.__values_dict['success'] = True

    except Exception as e:

      self.__values_dict['success'] = False
      self.__logger.error(f"::Scraper:: Error found; {e}")

    return self.__values_dict






  # # base_url = 'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/USA-CA-Pleasanton/Integrated-Business-Planning-Director_JR-62624'
# list_url = [
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/Canada-BC-Vancouver/QA-Engineer---Talent_JR-59819',
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/USA-CA-Pleasanton/Integrated-Business-Planning-Director_JR-62624',
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/Ireland-Dublin/Public-Cloud-Software-Development-Engineer_JR-57427',
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/Ireland-Dublin/Software-Developer-Network-Automation_JR-57626',
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/Ireland-Dublin/Site-Reliability-Engineer---Tenant-Lifecycle-Engineering_JR-65474',
#   'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/United-Kingdom-London/Channel-Operations-Analyst_JR-63806'
#
# ]


  #base_url = 'https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/Canada-BC-Vancouver/QA-Engineer---Talent_JR-59819'

  # print(response.text)
