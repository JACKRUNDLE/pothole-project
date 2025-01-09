import boto3
import json

from data_model import PotholeModel

#converts payload to json else returns origional json
def convert_to_json(data):
    try:
        payload = json.loads(data)
        return payload
    except Exception:
        return data

def lambda_handler(event, context):
    print(event)
    #get event data amd client
    
    payload = event.get("body")
    payload = convert_to_json(payload)
    long = float(payload.get("longitude"))
    lat = float(payload.get("latitude"))
    client = boto3.client('location')

    #format response with lat and long
    print("latitude: ", lat, ", longitude: ", long)

    response = client.search_place_index_for_position(
        IndexName='pothole-place-index',
        Language='en',
        MaxResults=1,
        Position=[long, lat]
    )
    print("response: ", response)
    address = json.dumps(response['Results'][0]['Place']['Label'])
    my_pothole = PotholeModel()
    my_pothole.from_raw(account_id=2, longitude=long, latitude=lat, address=address)
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
    
        
