import json
import boto3

# import requests
dynamodb = boto3.resource('dynamodb')
potholeTable = dynamodb.Table('PotholeDDB1')

def lambda_handler(event, context):

    response = potholeTable.scan()
    print(response)


    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
