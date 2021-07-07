# -*- coding: UTF-8 -*-

URLS = ['https://aig.wd1.myworkdayjobs.com/es/aig/job/NC-Charlotte/Cyber-Security-Solutions-Engineer_JR2103887',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/IN-Jeffersonville/Dispatcher_JR2104864',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/NY-New-York/AIG-Risk-Management-Finance-Director_JR2103486-2',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/NC-Charlotte/AUDIT-MANAGER_JR2102075-1',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/KS-Olathe/Customer-Advocate--Remote_JR2101952-1',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/IN-Jeffersonville/Senior-Claims-Examiner---Bilingual_JR2007296',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/One-Montgomery-Street-120-Kearny-Street-CA/Managing-Director-Business-Development--First-Principles-AIG_JR2103940',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/MA-Boston/Programs---Product-Line-Officer_JR2101885-1',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/NY-New-York/Global-Head-of-Business-Development-for-Warranty---Service-Programs_JR2104383',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/TX-Amarillo/In-Force-Management-Associate-Case-Review_JR2104507',
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/340-Seven-Springs-Way-Brentwood-TN/Financial-Advisor---Kingsport--TN--Tri-Cities-_JR2104584-2']

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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json,application/xml'
}
