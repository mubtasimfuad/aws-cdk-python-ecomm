import json

def lambda_handler(event, context):
    # Sample Lambda function handler
    # event: The event data passed to the Lambda function
    # context: The runtime information provided by Lambda (e.g., request ID, function name)

    # Sample request data (assumes the event is an HTTP API Gateway event)
    request_data = {
        "statusCode": 200,
        "body": "Hello, world!",
        "headers": {
            "Content-Type": "text/plain"
        }
    }

    # Return the response
    return request_data
