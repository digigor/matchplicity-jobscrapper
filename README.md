# TK-Digigor

This crawler was created to scrape information from a given job platform URL.
The data fields keeping in mind are the following:

- title : string
- description : string
- application_url : sting
- job_type : array|object
- preferred_years_experience : array|object [min, max]
- salary : numeric
- preferred_certification : array|object
- preferred_previous_job_title : string
- preferred_experience : integer
- preferred_soft_skill : array|object
- preferred_technical_skill : array|object
- job_preferred_major : array|object
- job_gpa : digit
- job_locations : array|object

### Strategy Used

- I used "Flask" to create an api that receives the parameters, 
make request and return a json with extracted data.
  
- Regarding the crawler, I used different kind of strategies. For each major platform I selected the best strategy. 
For instance, for myworkjobdays I used requests, and for Taleo I used selenium.
  
- The crawler receive a list of dict with key 'url' and execute as many threads configured on the "MAX_WORKERS" on the config.py.

Tested on Python 3.8

### How to use

1) go to the config.py and edit:

-PROXYSOCKET #if needed.
   
-MAX_WORKERS: this is the number of threads to be executed on parallel. 

-PORT: Set the port to be used on the API
    
2) install requirements doing:

```pip3 install -r requirements```.

3) execute```python3 app.py runserver```
    
#### Notes or Considerations

- For the taleo platform and the ones using Selenium the server will consume at least 500 mb of ram and as many cpu as needed, per instance.
So,if you have MAX_WORKERS = 10 and you execute 10 taleo urls the crawler will create 10 firefox instances.
  
- For the taleo platform the URL must have the 'job' key with a value at the bottom for instance:
  
```
https://ms.taleo.net/careersection/2/jobdetail.ftl?job=3183894
```

- if the job is no longer available the API will respond a msg on the "description" key called "the job is no longer available".
for instance:
  
```
  {
  "error_code": 0, 
  "msg": "Results obtained", 
  "results": [
    {
      "application_url": null, 
      "description": "the job is no longer available", 
      "job_gpa": null, 
      "job_locations": [], 
      "job_preferred_major": [], 
      "job_type": [], 
      "preferred_certification": [], 
      "preferred_previous_job_title": null, 
      "preferred_soft_skill": [], 
      "preferred_technical_skill": [], 
      "preferred_years_experience": [], 
      "salary": null, 
      "title": null
    }
  ], 
  "success": true
}
```
- If the url is a 404 error or not a 200 http status code, the API will respond: "Error_code": 404.

#### Example of usage:
```
curl --location --request POST 'http://151.80.33.51:6789/get-job' \
--header 'Content-Type: application/json' \
--data-raw '[
{
    "url": "https://ms.taleo.net/careersection/2/jobdetail.ftl?job=3163603"
},
{
    "url": "https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers/job/Costa-Rica---Escazu/Sr-Associate--Solution-and-Service-Management_4823561"
},
{
    "url": "https://ms.taleo.net/careersection/2/jobdetail.ftl?job=3183894"
},
{
    "url": "https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers/job/Belgium---Puurs/Technisch-Operator-Vaccin---3-ploegen_4782834"
}
]'
```
#### Changelog:

'Francisco Battan. Informatics Engineer.'
