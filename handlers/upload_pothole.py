import boto3
import json
import string

from data_model import PotholeModel

#converts payload to json else returns origional json
def convert_to_json(data):
    try:
        payload = json.loads(data)
        return payload
    except Exception:
        return data

def lambda_handler(event, context):
    #print(event)
    #get event data amd client
    try:
        payload = event.get("body")
        payload = convert_to_json(payload)
        acct_id = (payload.get("account_id"))
        long = float(payload.get("longitude"))
        lat = float(payload.get("latitude"))
    except Exception as e:
        print(f"Bad arguments: message={e}")
        return {
        "statusCode": 400,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Max-Age': '300'
        },
        "body": "Bad Arguments",
        }
 
    client = boto3.client('location')

    response = client.search_place_index_for_position(
        IndexName='pothole-place-index',
        Language='en',
        MaxResults=1,
        Position=[long, lat]
    )
    address = json.dumps(response['Results'][0]['Place']['Label'])
    my_pothole = PotholeModel()
    print("account id: ", acct_id)
    my_pothole.from_raw(account_id=acct_id, longitude=long, latitude=lat, address=address)
    my_pothole.to_dynamo()

    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Max-Age': '300'
        },
        "body": address,
    }
    
        
