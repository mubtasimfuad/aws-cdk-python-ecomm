# add dyanomo db client
import boto3 as client


ddb_client = client.client('dynamodb')

ddb_res_client = client.resource('dynamodb')
event_bridge_client = client.client("events")
