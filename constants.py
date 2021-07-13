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
        'https://aig.wd1.myworkdayjobs.com/en-US/aig/job/340-Seven-Springs-Way-Brentwood-TN/Financial-Advisor---Kingsport--TN--Tri-Cities-_JR2104584-2',
        'https://cliftonlarsonallen.wd1.myworkdayjobs.com/en-US/CLA/job/Green-Bay-WI/Audit-Intern-Spring-2022---Green-Bay--WI_R4447-1',
        'https://cliftonlarsonallen.wd1.myworkdayjobs.com/en-US/CLA/job/St-Louis-MO/Senior-Accountant_R5597',
        'https://cliftonlarsonallen.wd1.myworkdayjobs.com/en-US/CLA/job/Greenwood-Village-CO/Staff-Accountant---Nonprofit_R5862',
        'https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers/job/Austria---Orth/GMP-Training---Documentation-Junior-Specialist--m-f-d-_4818299-1',
        'https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers/job/Bulgaria---Bulgaria/Supply-Chain-Quality-Specialist--part-time-role--temporary-contract-_4818820-1',
        'https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers/job/United-States---Connecticut---Groton/DSRD-Graduate-Student-Internship_4801205',
        'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal/job/US-NJ-HOBOKEN-Home-Office-121-River-St/Principal-Software-Engineer---Chatbot_R-537659',
        'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal/job/CAN-BC-VICTORIA-03109-WM-SUPERCENTER/Customer-Experience_R-258146-1',
        'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal/job/US-AR-BENTONVILLE-Home-Office-ISD-Office---DGTC/Senior-Manager-I--Software-Engineering_R-645761-1',
        'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal/job/US-AR-BENTONVILLE-Home-Office-608-Building/Senior-Manager-II--Software-Engineering_R-588583-2',
        'https://boeing.wd1.myworkdayjobs.com/en-US/NABA/job/USA---Long-Beach-CA/Senior-C-17-Contracts-and-Pricing-Representative_00000241128-2',
        'https://boeing.wd1.myworkdayjobs.com/en-US/NABA/job/USA---Charleston-SC/Cost-Recovery-Analyst_00000247264-3',
        'https://roberthalf.wd1.myworkdayjobs.com/en-US/ProtivitiExperiencedCareers/job/TORONTO/Toronto-Internal-Audit-Financial-Advisory-Senior-Manager_JR-236098',
        'https://roberthalf.wd1.myworkdayjobs.com/RobertHalfStaffingCareers/job/MINNETONKA/Minnetonka-Accountemps-Staffing-Manager_JR-231971-1',
        'https://roberthalf.wd1.myworkdayjobs.com/RobertHalfStaffingCareers/job/MINNETONKA/Minnetonka-RH-Finance-and-Accounting-Recruiting-Manager_JR-232605',
        'https://roberthalf.wd1.myworkdayjobs.com/RobertHalfStaffingCareers/job/PORTLAND/Staffing-Manager--Accountemps---Portland_JR-232340/',
        'https://roberthalf.wd1.myworkdayjobs.com/RobertHalfStaffingCareers/job/NEW-YORK-MIDTOWN/Managing-Vice-President-Strategic-Accounts_JR-232642/',
        'https://roberthalf.wd1.myworkdayjobs.com/en-US/ProtivitiExperiencedCareers/job/DALLAS/Technology-Consulting-Digital-Identity--Okta-Architect--Senior-Manager_JR-235585']

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

INPUT_FILE = 'input.xlsx'
