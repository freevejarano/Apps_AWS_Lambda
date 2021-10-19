import urllib.request
import boto3
import time


def handler(event, context):
    local_time = time.localtime()

    s3 = boto3.resource('s3')
    downloadNews("Tiempo", "https://www.eltiempo.com/", "https://www.elespectador.com/", local_time, s3)
    downloadNews("")


def downloadNews(name, url, local_time, bucket, s3):
    query = urllib.request.urlopen(url)
    query = query.read()
    file = '/tmp/'+name+'.html'
    with open(file, 'wb') as web:
        web.write(query)
    data = {
        'file': file,
        'bucket': bucket,
        'path': f'headlines/raw/newspaper={name}/year={local_time.tm_year}/month={local_time.tm_mon}'
                f'/day={local_time.tm_mday}/{local_time.tm_hour}{local_time.tm_min}{local_time.tm_sec}page.html'
    }
    #s3.meta.client.upload_file(data['file'], data['bucket'], data['path'])