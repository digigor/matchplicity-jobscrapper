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

      if list_location:
        for loc in list_location:
          location =  self.update_location(loc, keywords_dict)
          print(location)





      self.__values_dict['success'] = True

    except Exception as e:

      self.__values_dict['success'] = False
      self.__logger.error(f"::Scraper:: Error found; {e}")

    return self.__values_dict

  def update_location(self, loc, keywords_dict):
    try:
      if "-" in loc:
        location = loc.split("-")
      elif "," in loc:
        location = loc.split(",")
      else:
        location = loc

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
          for sta, abrev in usa_states.us_state_to_abbrev.items():
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
        country = location[-0].lstrip(' ').rstrip(' ')
        if country == "USA":
          country = "United States"
          for sta, abrev in usa_states.us_state_to_abbrev.items():
            if abrev == state:
              state = sta


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

      # self.__values_dict['job_locations'].append(location_dict)
      return location_dict
    except Exception as e:
      pass


