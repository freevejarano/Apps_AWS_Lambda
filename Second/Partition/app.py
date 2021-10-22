import time
import boto3

def handler(event, context):
    DATABASE = 'webscraping'
    TABLE = 'news'
    S3_OUTPUT = 's3://news-big-data2021-2/LambdaParticion/'

    try:
        query = 'MSCK REPAIR TABLE `news`;'
        client = boto3.client('athena')

        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': DATABASE
            },
            ResultConfiguration={
                'OutputLocation': S3_OUTPUT,
            }
        )
        return {"statusCode": 200, "Body": "Save success", "response":response}
    except:
        return {"statusCode": 400, "Body": "Save fail"}