# -*- coding: UTF-8 -*-

PROXYSOCKET = ''

# MAX_WORKERS = 1
MAX_WORKERS = 10

RETRY_TIMES = 5

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json,application/xml'
}

INPUT_FILE = 'dependencies/input.xlsx'
LOCATIONS_FILE = 'dependencies/city_state_country_202109101841.csv'

API_DEBUG = True
API_PORT = 6789

POST_TIME = 60
PARAMETERS = {
    'headless': True,

}
