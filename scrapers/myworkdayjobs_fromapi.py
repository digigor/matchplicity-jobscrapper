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
    self.__regex_dict = {
      'Years of Experience':
        re.compile(r'(?:\s)(\d)(?: ?\+?-? (?:or more )?years.*?experience)', re.IGNORECASE),
      'Salary':
        re.compile(r'(?:salary.*?)(\$[\d.,]+ to \$[\d.,]+)(?:\.?)', re.IGNORECASE),
      'GPA':
        re.compile(r'(?:(?:minimum|minimum GPA|overall.*?GPA) (?:of )?)(\d\.\d{1,2})(?: degree| cumulative GPA)?',
                   re.IGNORECASE),
      'Virtual environment':
        re.compile(
          r'(virtual job|virtual.*?team|virtual remote|work at home|work-at-home|home office|remote work|virtual option|home based)',
          re.IGNORECASE),
      'Physical environment':
        re.compile(r'(physical office|physical environment|office based)', re.IGNORECASE),
      'Hybrid environment':
        re.compile(r'(hybrid environment|work at home/office|office and home|hybrid/work at home)', re.IGNORECASE),
      'internship': ['internship', 'Internship']
    }

  def scrape(self, job_url, keywords_dict):
    try:
      if 'workday.wd5' in job_url:
        job = re.findall(r'(?:job/)(.*)', job_url)[0]
        url_final = f"https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/job/{job}"
      elif 'alvarezandmarsal' in job_url:
        job = re.findall(r'(?:job/)(.*)', job_url)[0]
        url_final = f"https://alvarezandmarsal.wd1.myworkdayjobs.com/wday/cxs/alvarezandmarsal/alvarezandmarsalp/job/{job}"

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
      list_location_update = []
      if job_json['jobPostingInfo']['location']:
        location = self.update_location(job_json['jobPostingInfo']['location'], keywords_dict)
        list_location_update.append(location)
      try:
        if job_json['jobPostingInfo']['additionalLocations']:
          for loc in job_json['jobPostingInfo']['additionalLocations']:
            location = self.update_location(loc, keywords_dict)
            list_location_update.append(location)
      except Exception as e:
        pass
      self.__values_dict['job_locations'] = list_location_update


      self.__values_dict['success'] = True

      years_list = self.__regex_dict['Years of Experience'].findall(job_json['jobPostingInfo']['title'])
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
        keywords_dict['Certifications'], job_json['jobPostingInfo']['title']))

      aux = self.__regex_dict['Salary'].findall(job_json['jobPostingInfo']['title'])
      if aux:
        try:
          self.__values_dict['salary'] = aux[0]
        except Exception as e:
          pass

      if self.__tools_obj.search_keyword(keywords_dict['Titles'], job_json['jobPostingInfo']['title']):
        self.__values_dict['preferred_previous_job_title'] = self.__tools_obj.search_keyword(
          keywords_dict['Titles'], job_json['jobPostingInfo']['title'])

      if (self.__tools_obj.search_keyword(
              keywords_dict['Soft Skills'], job_json['jobPostingInfo']['title'])):
        self.__values_dict['preferred_soft_skill'] = (self.__tools_obj.search_keyword(
          keywords_dict['Soft Skills'], job_json['jobPostingInfo']['title']))

      if self.__tools_obj.search_keyword(
              keywords_dict['Technical Skills'], job_json['jobPostingInfo']['title']):
        self.__values_dict['preferred_technical_skill'] = self.__tools_obj.search_keyword(
          keywords_dict['Technical Skills'], job_json['jobPostingInfo']['title'])

      if self.__tools_obj.search_keyword(
              keywords_dict['Majors'], job_json['jobPostingInfo']['title']):
        self.__values_dict['job_preferred_major'] = self.__tools_obj.search_keyword(
          keywords_dict['Majors'], job_json['jobPostingInfo']['title'])

      aux = self.__regex_dict['GPA'].findall(job_json['jobPostingInfo']['title'])
      if aux:
        try:
          self.__values_dict['job_gpa'] = int(aux[0])
        except Exception as e:
          pass
    except Exception as e:

      self.__values_dict['success'] = False
      self.__logger.error(f"::Scraper:: Error found; {e}")

    return self.__values_dict

  def update_location(self, loc, keywords_dict):
    try:
      location = self.clean_location(loc)

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
        dict_aux ={
          'country': country,
          "state": None,
          "city": None
        }
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
            # else:
            #   dict_aux = {'country': country,
            #               'state': None,
            #               'city': aux}

        location_dict['country'] = dict_aux['country']
        location_dict['state'] = dict_aux['state']
        location_dict['city'] = dict_aux['city']

      elif len(location) == 3:
        city = location[-1].lstrip(' ').rstrip(' ')
        state = location[-2].lstrip(' ').rstrip(' ')
        country = location[-0].lstrip(' ').rstrip(' ')
        if country == "USA" or country == "US":
          country = "United States"
          for sta, abrev in usa_states.us_state_to_abbrev.items():
            if abrev == state:
              state = sta


        for loc in keywords_dict['locations']:
          if country in loc['country'] and state in loc['state'] and city in loc['city']:
            location_dict['country'] = loc['country']
            location_dict['state'] = loc['state']
            location_dict['city'] = loc['city']
            break
          elif country in loc['country'] and state in loc['state']:
            location_dict['country'] = country
            location_dict['state'] = state
            location_dict['city'] = city
            break
          elif country in loc['country'] and city in loc['city']:
            location_dict['country'] = country
            location_dict['state'] = loc['state']
            location_dict['city'] = city
            break
          else:
            location_dict['country'] = country
            location_dict['state'] = state
            location_dict['city'] = city


      # self.__values_dict['job_locations'].append(location_dict)
      return location_dict
    except Exception as e:
      pass

  def clean_location(self, loc):
    try:
      # split for '-'
      if "-" in loc:
        aux_location = []
        list_split_location = loc.split("-")
        for locat in list_split_location:
          if "," in locat:
            sublist_locat = locat.split(",")
            aux_location.extend(sublist_locat)
          else:
            aux_location.append(locat)
        if len(aux_location) == 3:
          aux = aux_location[1]
          aux_location[1] = aux_location[2]
          aux_location[2] = aux
        location = aux_location

      # split for ','
      elif "," in loc:
        location = loc.split(",")
      else:
        location = []
        location.append(loc)
      return location
    except Exception as e:
      return loc

