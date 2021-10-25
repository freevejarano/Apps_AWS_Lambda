import requests
import boto3
import time


def handler(event, context):
    try:
        local_time = time.localtime()
        s3 = boto3.resource('s3')
        bucket = "news-big-data2021-1"
        downloadNews("El_Tiempo", "https://www.eltiempo.com/", local_time, bucket, s3)
        downloadNews("El_Espectador", "https://www.elespectador.com/", local_time, bucket, s3)
        return {"statusCode": 200, "Body": "Successful Download"}
    except:
        return {"statusCode": 400, "Body": "Failed Download"}

def downloadNews(name, url, local_time, bucket, s3):
    query = requests.get(url)
    file = '/tmp/'+name+'.html'
    with open(file, 'w') as web:
        web.write(query.text)
    data = {
        'file': file,
        'bucket': bucket,
        'path': f'headlines/raw/newspaper={name}/year={local_time.tm_year}/month={local_time.tm_mon}'
                f'/day={local_time.tm_mday}/{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}page.html'
    }
    s3.meta.client.upload_file(data['file'], data['bucket'], data['path'])

