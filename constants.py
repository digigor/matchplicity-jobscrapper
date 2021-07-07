# -*- coding: UTF-8 -*-

URLS = ['https://aig.wd1.myworkdayjobs.com/aig',
        'https://cliftonlarsonallen.wd1.myworkdayjobs.com/en-US/CLA',
        'https://humana.wd5.myworkdayjobs.com/en-US/Humana_External_Career_Site/',
        'https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers',
        'https://roberthalf.wd1.myworkdayjobs.com/en-US/ProtivitiExperiencedCareers',
        'https://protiviti.recsolu.com/job_boards/S29cfuRzXlvTQNWy1ttINA',
        'https://boeing.wd1.myworkdayjobs.com/NABA',
        'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal']

PROXYFLOW_URL = 'https://api.proxyflow.io/v1/proxy/random?token=ef54cdc884ff94d624e0f4e3&ssl=true&protocol=http'

PARAMETERS = {
    'waitTime': 1,
    'waitTime2': 2,
    'waitMaxTime': 20,
    'waitingTime': 5,
    'waitRetryTime': 90,
    'headless': True,
    # stormproxies/proxyflow
    'proxyType': 'stormproxies',
    'proxySocket': '104.194.139.168:3199'
}

RETRY_TIMES = 5

ANTICAPTCHA_KEY = '66ca75483fcda5a6dbbda8ffa404e2a3'
