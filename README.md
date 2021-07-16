# TK-Digigor

This crawler was created to extract job info in different pages.

### Strategy Used

I used "Flask" to create an api that receives the parameters, 
make request and return a json with extracted data.

#### Dependencies

* pandas
* openpyxl
* flask
* flask_cors
* requests

Tested on Python 3.8

### How to use

1) Edit proxy:
    - sudo nano /tk-digigor/config.py
    
2) Run api:
    - python3 /tk-digigor/app.py runserver
    
#### Notes or Considerations

You can pass as many url you want, changing the name of parameter. 
Requests example:
* curl --location --request GET 'http://127.0.0.1:5678/get-job?
  url=https://aig.wd1.myworkdayjobs.com/aig/job/TX-Amarillo/Commissions-Processor_JR2104121&
  url2=https://aig.wd1.myworkdayjobs.com/aig/job/NY-New-York/Home-Office-Claims-Consultant-Group-Lead_JR2100779&
  url3=https://aig.wd1.myworkdayjobs.com/aig/job/Singapore/Complex-Claims-Adjuster---Auto_JR2101051'
  
#### Changelog:

'Francisco Battan. Informatics Engineer.'
