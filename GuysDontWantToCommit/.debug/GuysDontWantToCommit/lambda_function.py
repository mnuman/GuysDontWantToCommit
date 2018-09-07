import boto3
import json
import os
import requests

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name ='SecretYammerToken', WithDecryption=True)
oauthHeader = { "Authorization" : "Bearer " + parameter['Parameter']['Value']}

def lambda_handler(event, context):
    body = json.loads(event['body'])

    myMessage = f"Hi, {body['head_commit']['author']['name']} has just committed code at {body['head_commit']['url']} with message {body['head_commit']['message']}"
    payload = { "body" : myMessage, "group_id" : os.environ['YAMMER_GROUP_ID']}
    r = requests.post("https://www.yammer.com/api/v1/messages.json", headers=oauthHeader, data=payload)
    return {
        "isBase64Encoded" :"false",
        "statusCode" : r.status_code,
        "headers" : {},
        "body" : "Acknowledge receiving webhook request"
    }