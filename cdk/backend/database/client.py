# add dyanomo db client
from aws_cdk import boto3 as client

client = client.resource('dynamodb')