import requests
import json
import os
import pandas as pd
from pandas import DataFrame
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime
from IPython.display import HTML
from smtplib import SMTP
import smtplib
import sys
import win32com.client as win32
import matplotlib.pyplot as plt
import xlsxwriter
import re
import requests
import json
import smtplib
import sys
import traceback
import email
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders
import matplotlib.dates as mdates
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

array=[]
def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

count=1

response = requests.get('http://usmlvv1hdx773:9000/api/issues/search').json()

fromDate = date.today() + relativedelta(weeks=-2)
print("Issues are getting displayed since :"+ str(fromDate))
print("Today's date :" +str(date.today()))

df = pd.DataFrame({"Sl_No":[], "Issue_Date":[], "Project":[], "Severity":[], "Status":[], "File Name":[],"Issue_Type":[], "Issue":[], "Issue_Age":[]})
pd.set_option('display.max_colwidth', 100)
for i in response["issues"]:    
    updateDate = i["updateDate"]
    issueDate = datetime.datetime.strptime(updateDate[:10], "%Y-%m-%d").date()
    subProject = i["subProject"]
    severity = i["severity"]
    componentData = i["component"]
    message = i["message"]
    status = i["status"]
    issueType = i["type"]
        
    if(issueDate>=fromDate and status=='OPEN'):
        issueAge = (date.today() - issueDate).days
        #print(issueAge)
        df=df.append({"Sl_No":str(count), "Issue_Date":change_date_format(str(issueDate)), "Project":subProject[subProject.find(":")+1:], "Issue_Type":issueType, "Severity":severity, "Status":status, "File Name":componentData, "Issue":message, "Issue_Age":str(issueAge)+"days"}, ignore_index=True)
        array.append(issueDate)
        count+=1
    
print("The total number of issues : " + str(count-1))
df = df[["Sl_No", "Issue_Date", "Project", "Severity", "Status", "File Name","Issue_Type", "Issue", "Issue_Age"]]

print(len(array))

date_time = array
date_time = pd.to_datetime(date_time)
temp = [2, 4, 6, 4, 6, 3,2, 4, 6, 4, 6, 3,2, 4, 6, 4, 6, 3,9,4,2,4,7 ]

DF = pd.DataFrame()
DF['temp'] = temp
DF = DF.set_index(date_time)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.10)
plt.title('Trend Analysis')
plt.xlabel('Dates')
plt.ylabel('No. of Issues')
plt.xticks(rotation=90)
plt.plot(DF)
plt.tight_layout()
plt.savefig('C:\\Users\\ad040730\\Documents\\Trend_Analysis.png')
print('Graph saved')

def color_negative_red(value):
    color = 'red' if value <9 else 'blue'
    return 'color: %s' % color

df.style.applymap(color_negative_red)


writer = pd.ExcelWriter("C:\\Users\\ad040730\\Documents\\SonarReport.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name="Sheet 1", index=False)
workbook  = writer.book
worksheet = writer.sheets['Sheet 1']
worksheet.set_column(1,10,15)   
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num , value, header_format)

writer.save()
print("Data copied as excel file")

try:
    sender = 'dipannita.basu@cerner.com'
    receivers = ['alak.das@cerner.com']
    msg = MIMEMultipart('mixed')
    msg['Subject'] = ('Sonar Report since '+ str(fromDate))
    print(('Sonar Report since '+ str(fromDate)))
        
    print("Starting mail body part")
    
    dataFrame = '''
               <h3>The Sonar issues since last 14 days.</h3>
               <img src="C:\\Users\\ad040730\\Documents\\Trend_Analysis.png"></img> 
               {}
               <h3>Thanks</h3>
               '''.format(df.to_html(na_rep = "", index = False).replace('<th>','<th style = "background-color: #D7E4BC">'))
    
    
    img_data = open('C:\\Users\\ad040730\\Documents\\Trend_Analysis.png', 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename('C:\\Users\\ad040730\\Documents\\Trend_Analysis.png'))
    msg.attach(image)
    
    htmlBody = MIMEText(dataFrame, 'html') 
    msg.attach(htmlBody)
    
    print("Attaching")
    filename = "SonarReport.xlsx"
    filepath = "C:\\Users\\ad040730\\Documents\\SonarReport.xlsx"
    print("Taking filename")
    attachment = MIMEBase('application', "octet-stream")
    print("Attachment Step 2")
    attachment.set_payload(open(filepath, "rb").read())
    print("Attachment Step 3")
    encoders.encode_base64(attachment)
    print("Attachment Step 4")
    attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    print("Attachment Step 5")
    msg.attach(attachment)
    
    
    smtpObj = smtplib.SMTP('smtprr.cerner.com:25')
    print("Tested login")
    smtpObj.sendmail('dipannita.basu@cerner.com',['nalanda.chakrabarti@cerner.com', 'dipannita.basu@cerner.com', 'rahul.roy@cerner.com', 'alak.das@cerner.com'], msg.as_string())         
    print ("Successfully sent email")
    smtpObj.quit()
    
except Exception:
    print ("Error: unable to send email")
    print (traceback.format_exc())