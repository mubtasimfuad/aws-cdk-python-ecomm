import json
import os
from client import ddb_client, ddb_res_client, event_bridge_client, ddb_type
import traceback
from utils import DecimalEncoder


def lambda_handler(event, context):
    print("request:", json.dumps(event, indent=2))

    try:
        http_method = event["httpMethod"]
        if http_method == "GET":
            if event.get("pathParameters") is not None:
                body = get_basket(
                    event["pathParameters"]["userName"]
                )  # GET /basket/{userName}
            else:
                body = get_all_baskets()  # GET /basket
        elif http_method == "POST":
            if event.get("path") == "/basket/checkout":
                body = checkout_basket(event)  # POST /basket/checkout
            else:
                body = create_basket(event)  # POST /basket
        elif http_method == "DELETE":
            body = delete_basket(
                event["pathParameters"]["userName"]
            )  # DELETE /basket/{userName}
        else:
            raise Exception(f"Unsupported route: {http_method}")

        print(body)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": f"Successfully finished operation: {http_method}",
                    "body": body,
                },
                cls=DecimalEncoder,
            ),
        }

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

def get_basket(user_name):
    print("getBasket")
    try:
        # Get the DynamoDB table
        table_name = os.environ["DYNAMODB_TABLE_NAME"]
        table = ddb_res_client.Table(table_name)

        # Use the table's get_item method to retrieve the item
        response = table.get_item(Key={"userName": user_name})
        item = response.get("Item")
        return item if item is not None else {}

    except Exception as e:
        print(e)
        raise e

def get_all_baskets():
    print("getAllBaskets")
    try:
        params = {"TableName": os.environ["DYNAMODB_TABLE_NAME"]}
        print("params", params)
        response = ddb_client.scan(**params)
        items = response.get("Items")
        return items if items is not None else []

    except Exception as e:
        print(e)
        raise e


def create_basket(event):
    print("createBasket function. event:", event)
    try:
        request_body = json.loads(event["body"])
        user_name = request_body.get("userName", "")
        items = request_body.get("items", [])

        basket_data = {
            "userName": {"S": user_name},
            "items": {"L": [
                {
                    "M": {
                        "quantity": {"N": str(item.get("quantity", 0))},
                        "color": {"S": item.get("color", "")},
                        "price": {"N": str(item.get("price", 0))},
                        "productId": {"S": item.get("productId", "")},
                        "productName": {"S": item.get("productName", "")},
                    }
                }
                for item in items
            ]},
        }

        params = {
            "TableName": os.environ["DYNAMODB_TABLE_NAME"],
            "Item": basket_data,
        }
        
        response = ddb_client.put_item(**params)
        print(response)
        return response

    except Exception as e:
        print(e)
        raise e


def delete_basket(user_name):
    print("deleteBasket function. userName:", user_name)
    try:
        params = {
            "TableName": os.environ["DYNAMODB_TABLE_NAME"],
            "Key": {"userName": {"S": user_name}},
        }
        response = ddb_client.delete_item(**params)
        print(response)
        return response

    except Exception as e:
        print(e)
        raise e


def checkout_basket(event):
    print("checkoutBasket")

    # expected request payload: { userName: swn, attributes[firstName, lastName, email, ...] }
    checkout_request = json.loads(event["body"])
    if checkout_request is None or "userName" not in checkout_request:
        raise Exception(f"userName should exist in checkoutRequest: {checkout_request}")

    # 1- Get existing basket with items
    basket = get_basket(checkout_request["userName"])

    # 2- Create an event JSON object with basket items,
    # calculate total price, prepare order create JSON data to send to ordering ms
    checkout_payload = prepare_order_payload(checkout_request, basket)

    # 3- Publish an event to EventBridge - this will be subscribed by the order microservice and start the ordering process.
    published_event = publish_checkout_basket_event(checkout_payload)

    # 4- Remove existing basket
    delete_basket(checkout_request["userName"])


def prepare_order_payload(checkout_request, basket):
    print("prepareOrderPayload")

    try:
        if basket is None or "items" not in basket:
            raise Exception(f"basket should exist in items: {basket}")

        # Calculate totalPrice
        total_price = 0
        for item in basket["items"]:
            # Access nested attributes using DynamoDB types
            price = int(item["price"])
            total_price += price

        checkout_request["totalPrice"] = total_price
        print(checkout_request)

        # Extract the basket items as a list of dictionaries
        basket_items = basket["items"]

        # Update the basket dictionary with the extracted items
        checkout_request["items"] = basket_items

        print("Success prepareOrderPayload, orderPayload:", checkout_request)
        return checkout_request

    except Exception as e:
        print(e)
        raise e




def publish_checkout_basket_event(checkout_payload):
    print("publishCheckoutBasketEvent with payload:", checkout_payload)
    try:
        # EventBridge parameters for setting event to target system
        params = {
            "Entries": [
                {
                    "Source": os.environ["EVENT_SOURCE"],
                    "Detail": json.dumps(checkout_payload, cls=DecimalEncoder),
                    "DetailType": os.environ["EVENT_DETAILTYPE"],
                    "EventBusName": os.environ["EVENT_BUSNAME"],
                },
            ],
        }

        response = event_bridge_client.put_events(**params)
        print("Success, event sent; requestID:", response)
        return response

    except Exception as e:
        print(e)
        raise e
