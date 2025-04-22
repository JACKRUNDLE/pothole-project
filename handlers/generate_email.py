import boto3
import json
from boto3.dynamodb.conditions import Attr

from data_model import PotholeModel

client = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')
potholeTable = dynamodb.Table('PotholeDDB2')

GOOGLE_MAPS_API_KEY = ""
DESTINATION_EMAIL = ""
SOURCE_EMAIL = ""


def convert_to_json(data):
    try:
        return json.loads(data)
    except Exception:
        return data

def generate_static_map_url(latitude, longitude):
    """Generate Google Static Maps API URL for a snapshot."""
    return f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=15&size=600x300&markers=color:red|{latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}"

def gather_data(id):
    response = potholeTable.scan(FilterExpression=Attr("account_id").eq(id))
    pothole_info = []
    count = 1

    for item in response.get("Items", []):
        my_pothole = PotholeModel()
        my_pothole.from_item(item)
        my_pothole.process_data()

        # Extract data
        address = my_pothole.address
        latitude = my_pothole.latitude
        longitude = my_pothole.longitude
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        static_map_url = generate_static_map_url(latitude, longitude)

        # Store in list
        pothole_info.append({
            "count": count,
            "address": address,
            "maps_link": google_maps_link,
            "image_url": static_map_url
        })
        count += 1

        my_pothole.to_dynamo()

    return pothole_info

def lambda_handler(event, context):
    payload = event.get("body")
    payload = convert_to_json(payload)
    acct_id = payload.get("account_id")

    pothole_data = gather_data(acct_id)

    if not pothole_data:
        return {
            "statusCode": 200,
            "body": "No potholes found for this account."
        }

    # Construct HTML email with images
    email_body = "<html><body>"
    email_body += f"<h2>Pothole Report for Account {acct_id}</h2>"

    for pothole in pothole_data:
        email_body += f"""
        <p><strong>Pothole {pothole['count']} found at:</strong> {pothole['address']}</p>
        <a href="{pothole['maps_link']}">
            <img src="{pothole['image_url']}" alt="Pothole Location" width="600">
        </a>
        <p><a href="{pothole['maps_link']}">View on Google Maps</a></p>
        <hr>
        """

    email_body += "</body></html>"

    # Send email via AWS SES
    response = client.send_email(
        Destination={
            'ToAddresses': [DESTINATION_EMAIL],
        },
        Message={
            'Body': {
                'Html': {  # Ensure email is HTML formatted
                    'Charset': 'UTF-8',
                    'Data': email_body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': f'USER {acct_id}: Pothole Report',
            },
        },
        Source=SOURCE_EMAIL,
    )

    print(f"response: {response}")

    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Max-Age': '300'
        },
        "body": "Email sent with pothole locations and map snapshots.",
    }

        
