import builtins
import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct


class eShadhinDatabase(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
        # product table
        self.product_table = self.create_product_table()
        # basket table
        self.basket_table = self.create_basket_table()
        # order table
        self.order_table = self.create_order_table()

    def create_product_table(self):
        table = dynamodb.Table(
            self,
            "ProductTable",
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
        return table

    def create_basket_table(self):
        basket_table = dynamodb.Table(
            self,
            "basket",
            partition_key=dynamodb.Attribute(
                name="userName",
                type=dynamodb.AttributeType.STRING,
            ),
            table_name="basket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        return basket_table

        # Order DynamoDB Table Creation
        # order: PK: userName, SK: orderDate

    def create_order_table(self):
        order_table = dynamodb.Table(
            self,
            "order",
            partition_key=dynamodb.Attribute(
                name="userName",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="orderDate",
                type=dynamodb.AttributeType.STRING,
            ),
            table_name="order",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        return order_table
