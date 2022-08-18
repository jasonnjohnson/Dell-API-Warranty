from urllib import response
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

#vars used to store Dell TechDirect creds stored in .env file
CLIENT_ID = os.environ.get("Client_ID")
CLIENT_SECRET = os.environ.get("Client_Secret")
GRANT_TYPE = os.environ.get("Grant_Type")

#Parameters used to pass in request header
params = {
    "grant_type": GRANT_TYPE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

#Fuction to get Dell TechDirect Access Token
def authenticate():

    #Endpoint to get OAuth token
    endpoint = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"

    response = requests.post(endpoint, data=params)

    if response.status_code == 200:
        try:
            return response.json()
        except:
            return response.text
    else:
        return vars(response)


#Read in asset csv of Dell service tag numbers
def open_file():
    df = pd.read_csv('/Users/johnson.3279/Documents/DellApi/shs_assets.csv')
    servicetags = df.to_dict()
    return servicetags

def getWarranty():
    #Call authenicate() to get Access Token
    token = authenticate()
    
    #Set Auth token
    headers = {"Authorization": "Bearer " + token['access_token']}

    #Call open_file() to read in Dell service tags from a .csv
    servicetags = open_file()

    #Endpoint to get warranty info based on Dell Service Tag
    endpoint = "https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements"
    
    
    for tag in servicetags:
        
        response = requests.get(endpoint, params= {"servicetags": tag}, headers=headers)
        
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return response.text
        else:
             return vars(response)

print(getWarranty())