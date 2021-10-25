from datetime import datetime, timedelta
import csv
import urllib.request
from io import StringIO
import json
import boto3
import os

def handler(event,context):
    
    # Obtain of dates
    dateToday = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dateYesterday = dateToday - timedelta(days=1) #1
    dateYesterday2 = dateToday - timedelta(days=2) #2

    # Conversion to timestamp 
    ts1 = round(datetime.timestamp(dateYesterday2))
    ts2 = round(datetime.timestamp(dateYesterday))

    # Data Companies
    name_companies = ["AVHOQ","EC","AVAL","CMTOY"]

    # Scraping to get csv
    for company in name_companies :

	#Reading
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{company}?period1={ts1}&period2={ts2}&interval=1d&events=history&includeAdjustedClose=true'
        print(url)
        urllib.request.urlretrieve(url,f"/tmp/{company}")

	#Storage
        finalUrl=f'stocks/company={company}/year={dateYesterday.year}/month={dateYesterday.month}/day={dateYesterday.day-1}/Actions_{company}.csv'
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(f'/tmp/{company}', 'bucketyahoo01',finalUrl)        

    return{
        "statusCode":200,
        "body":json.dumps("Hello from Lambda")
    }