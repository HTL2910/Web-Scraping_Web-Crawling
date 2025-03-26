import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import email.utils
import pandas as pd

api_url='https://remoteok.com/api/'
user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
REQUEST_HEADER={
    'User-Agent':user_agent,
    'Accept-Language':'en-US,en;q=0.5',

}

def get_job_posting():
    res=requests.get(api_url,headers=REQUEST_HEADER)
    return res.json()

def output_job_to_excel(data):
    wb=Workbook()
    job_sheet=wb.add_sheet("Jobs")
    header=list(data[0].keys())
    for i in range(len(header)):
        job_sheet.write(0,i,header[i])
    # wb.save('remoteok_data.xls')
    for i in range(len(data)):
        dataRow=data[i]
        values=list(dataRow.values())
        for j in range(len(values)):
            job_sheet.write(i+1,j,values[j])
    wb.save('remoteok_data.xls')
    
def scrap(start,end):
    json=get_job_posting()[int(start):int(end)]
    output_job_to_excel(json)
    print(pd.DataFrame(json)['company'])

if __name__=="__main__":
    scrap(1,30)
    
