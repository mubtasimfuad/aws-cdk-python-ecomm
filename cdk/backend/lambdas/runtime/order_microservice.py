import json
from botocore.exceptions import ClientError
import datetime
import os
import traceback
from client import ddb_res_client,ddb_client
from utils import DecimalEncoder, convert_to_python


def lambda_handler(event, context):
    print("request:", json.dumps(event, indent=2))

    if "Records" in event:
        # SQS Invocation
        sqs_invocation(event)
    elif "detail-type" in event:
        # EventBridge Invocation
        event_bridge_invocation(event)
    else:
        # API Gateway Invocation -- return sync response
        return api_gateway_invocation(event)


def sqs_invocation(event):
    print("sqsInvocation function. event :", json.dumps(event))

    for record in event["Records"]:
        print("Record:", json.dumps(record))
        checkout_event_request = json.loads(record["body"])

        # Create order item into DB
        create_order(checkout_event_request["detail"])


def event_bridge_invocation(event):
    print("eventBridgeInvocation function. event :", json.dumps(event))

    # Create order item into DB
    create_order(event["detail"])


def create_order(basket_checkout_event):
    try:
        print("createOrder function. event:", json.dumps(basket_checkout_event))

        # Extract the basket items as a list of dictionaries
        basket_items = basket_checkout_event["items"]

        print("basket_checkout_event :", json.dumps(basket_checkout_event))
        # Set orderDate for SK of order DynamoDB
        orderDate = datetime.datetime.utcnow().isoformat()
        basket_checkout_event["orderDate"] = orderDate

        # Your code to put_item into DynamoDB using the ddb_res_client
        order_table = ddb_res_client.Table(os.environ["DYNAMODB_TABLE_NAME"])
        response = order_table.put_item(Item=basket_checkout_event)
        print("PutItem response:", response)

        return "Order created successfully."

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Failed to perform operation.",
                    "errorMsg": str(e),
                    "errorStack": traceback.format_exc(),
                }
            ),
        }


        # Create order item into DB by dd resource client
        



def api_gateway_invocation(event):
    try:
        # GET /order
        # GET /order/{userName}
        if event["httpMethod"] == "GET":
            if event.get("pathParameters"):
                return get_order(event)
            else:
                return get_all_orders()
        else:
            raise Exception(f"Unsupported route: \"{event['httpMethod']}\"")

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Failed to perform operation.",
                    "errorMsg": str(e),
                    "errorStack": traceback.format_exc(),
                }
            ),
        }


def get_order(event):
    print("getOrder")

    try:
        # Expected request: xxx/order/swn?orderDate=timestamp
        userName = event["pathParameters"]["userName"]
        orderDate = event["queryStringParameters"]["orderDate"]

        # Get the order table using the ddb_res_client (ServiceResource)
        order_table = ddb_res_client.Table(os.environ["DYNAMODB_TABLE_NAME"])

        # Perform the query using the table resource
        response = order_table.query(
            KeyConditionExpression="userName = :userName and orderDate = :orderDate",
            ExpressionAttributeValues={":userName": userName, ":orderDate": orderDate},
        )

        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Failed to perform operation.", "errorMsg": str(e)}
            ),
        }


    


def get_all_orders():
    print("getAllOrders")
    try:
        table_name = os.environ["DYNAMODB_TABLE_NAME"]
        table = ddb_res_client.Table(table_name)
        response = table.scan()
        items = response.get("Items", [])
        

        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Failed to perform operation.",
                    "errorMsg": str(e),
                    "errorStack": traceback.format_exc(),
                }
            ),
        }
