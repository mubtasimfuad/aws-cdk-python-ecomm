# add dyanomo db client
import boto3 as client
import boto3.dynamodb.types as dynamodb_types

ddb_client = client.client('dynamodb')

ddb_res_client = client.resource('dynamodb')
event_bridge_client = client.client("events")
ddb_type = dynamodb_types
