import boto3
import json
from boto3.dynamodb.conditions import Attr

from data_model import PotholeModel
dynamodb = boto3.resource('dynamodb')
potholeTable = dynamodb.Table('PotholeDDB2')


#converts payload to json else returns origional json
def convert_to_json(data):
    try:
        payload = json.loads(data)
        return payload
    except Exception:
        return data
    

def lambda_handler(event, context):
    payload = event.get("body")
    payload = convert_to_json(payload)
    acct_id = (payload.get("account_id"))
    response = potholeTable.scan(FilterExpression=Attr("account_id").eq(acct_id))
    address_list = []
    for item in response.get("Items"):
        my_pothole = PotholeModel()
        my_pothole.from_item(item)
        my_pothole.process_data()
        print("item: ", my_pothole.address)
        address_list.append(my_pothole.address)
        my_pothole.to_dynamo()

    
    
    # print("response: ", response)
    # address = json.dumps(response['Results'][0]['Place']['Label'])
    # my_pothole = PotholeModel()
    # my_pothole.from_raw(account_id=2, longitude=long, latitude=lat, address=address)
    # my_pothole.to_dynamo()

    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Max-Age': '300'
        },
        "body": json.dumps(address_list),
    }
    
        
