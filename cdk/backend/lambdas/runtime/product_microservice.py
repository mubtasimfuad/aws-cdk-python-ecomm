import json
import os
import uuid
import traceback
from client import ddb_res_client as client
from utils import DecimalEncoder

table_name = os.environ["PRODUCT_TABLE_NAME"]
table = client.Table(table_name)


def lambda_handler(event, context):
    print("request:", json.dumps(event, indent=2))

    try:
        http_method = event["httpMethod"]
        if http_method == "GET":
            if (
                "queryStringParameters" in event
                and event["queryStringParameters"] is not None
            ):
                body = get_products_by_category(
                    event
                )  # GET product/1234?category=Phone
            elif "pathParameters" in event and event["pathParameters"] is not None:
                body = get_product(event["pathParameters"]["id"])  # GET product/{id}
            else:
                body = get_all_products()  # GET product
        elif http_method == "POST":
            body = create_product(event)  # POST /product
        elif http_method == "DELETE":
            body = delete_product(event["pathParameters"]["id"])  # DELETE /product/{id}
        elif http_method == "PUT":
            body = update_product(event)  # PUT /product/{id}
        else:
            raise ValueError(f"Unsupported route: {http_method}")

        print(body)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": f'Successfully finished operation: "{http_method}"',
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


def get_product(product_id):
    print("get_product")
    try:
        response = table.get_item(Key={"id": product_id})
        item = response.get("Item", None)
        return item if item else {}

    except Exception as e:
        print(e)
        raise e


def get_all_products():
    print("get_all_products")
    try:
        response = table.scan()
        items = response.get("Items", [])
        return [item for item in items]

    except Exception as e:
        print(e)
        raise e


def create_product(event):
    print("create_product")
    try:
        product_request = json.loads(event["body"])
        # Set product ID using UUID
        product_id = str(uuid.uuid4())
        product_request["id"] = product_id

        response = table.put_item(Item=product_request)
        return response

    except Exception as e:
        print(e)
        raise e


def delete_product(product_id):
    print("delete_product")
    try:
        response = table.delete_item(Key={"id": product_id})
        return response

    except Exception as e:
        print(e)
        raise e


def update_product(event):
    print("update_product")
    try:
        request_body = json.loads(event["body"])
        obj_keys = list(request_body.keys())

        update_expression = f"SET {', '.join(f'#key{index} = :value{index}' for index, _ in enumerate(obj_keys))}"
        expression_attribute_names = {
            f"#key{index}": key for index, key in enumerate(obj_keys)
        }
        expression_attribute_values = {
            f":value{index}": request_body[key] for index, key in enumerate(obj_keys)
        }

        response = table.update_item(
            Key={"id": event["pathParameters"]["id"]},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
        )

        return response

    except Exception as e:
        print(e)
        raise e


def get_products_by_category(event):
    print("get_products_by_category")
    try:
        # GET product/1234?category=Phone
        product_id = event["pathParameters"]["id"]
        category = event["queryStringParameters"]["category"]

        response = table.query(
            KeyConditionExpression="id = :product_id",
            FilterExpression="contains (category, :category)",
            ExpressionAttributeValues={
                ":product_id": product_id,
                ":category": category,
            },
        )

        items = response.get("Items", [])
        return [item for item in items]

    except Exception as e:
        print(e)
        raise e
