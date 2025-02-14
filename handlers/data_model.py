import json
import boto3
import time
import random
import string

# import requests

dynamodb = boto3.resource('dynamodb')
potholeTable = dynamodb.Table('PotholeDDB2')

class PotholeModel(object):

    #initialize class empty
    def __init__(self): 
        self.pothole_id:str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.account_id:str = ""
        self.longitude:float = 0.0
        self.latitude:float = 0.0
        self.time:int = 0
        self.address:str = ""
        self.processed:int = 0
    
    #initialize class with data
    def from_raw(self, account_id:str, longitude:float, latitude:float, address:str):
        self.account_id = account_id
        self.longitude = longitude
        self.latitude = latitude
        self.time = int(time.time())
        self.address = address

    
    def process_data(self):
        self.processed:int = int(time.time())
        

    #get object from the database using primary key
    def from_dynamo(self, pothole_id:str):
        response = potholeTable.get_item(Key = {"pothole_id": pothole_id})
        self.from_item(response.get("Item"))

    #helper function for from_dynamo
    def from_item(self, item):
        self.pothole_id = item.get("pothole_id")
        self.account_id = str(item.get("account_id"))
        self.longitude = float(item.get("longitude"))
        self.latitude = float(item.get("latitude"))
        self.time = item.get("time")
        self.address = item.get("address")
        self.processed = item.get("processed")

    #return address
    def to_dict(self):
        return {
            "pothole_id": self.pothole_id,
            "account_id": self.account_id,
            "longitude": str(self.longitude),
            "latitude": str(self.latitude),
            "time": self.time,
            "address": self.address,
            "processed": self.processed
        }
    
    #pushes class object to dynamo
    def to_dynamo(self):
        response = potholeTable.put_item(Item = self.to_dict())
        return(response)

    
   