import os
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_lambda as lambda_


class eShadhinLambda(Construct):
    def __init__(self, scope: Construct, id: str, db) -> None:
        super().__init__(scope, id)

        self.product_lambda = self.create_product_lambda(db.product_table)
        self.basket_lambda = self.create_basket_lambda(db.basket_table)
        self.order_lambda = self.create_ordering_lambda(db.order_table)
        # get db value

    def create_product_lambda(self, product_table):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        product_lambda = lambda_.Function(
            self,
            "ProductLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="product_microservice.lambda_handler",
            code=lambda_.Code.from_asset(os.path.join(current_dir, "runtime")),
            memory_size=128,
        )
        # add permission to lambda

        product_table.grant_read_write_data(product_lambda)
        return product_lambda

    def create_basket_lambda(self, basket_table):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        basket_function = lambda_.Function(
            self,
            "BasketLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="basket_microservice.lambda_handler",
            code=lambda_.Code.from_asset(os.path.join(current_dir, "runtime")),
            memory_size=128,
            environment={
                "PRIMARY_KEY": "userName",
                "DYNAMODB_TABLE_NAME": basket_table.table_name,
                "EVENT_SOURCE": "com.shadhin.basket.checkoutbasket",
                "EVENT_DETAILTYPE": "CheckoutBasket",
                "EVENT_BUSNAME": "eShadhinEventBus",
            },
        )

        basket_table.grant_read_write_data(basket_function)
        return basket_function

    def create_ordering_lambda(self, order_table):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ordering_function = lambda_.Function(
            self,
            "OrderingLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="order_microservice.lambda_handler",
            code=lambda_.Code.from_asset(
                os.path.join(current_dir, "runtime")
            ),  # Assuming your code is in a "src" directory
            memory_size=128,
            environment={
                "PRIMARY_KEY": "userName",
                "SORT_KEY": "orderDate",
                "DYNAMODB_TABLE_NAME": order_table.table_name,
            },
        )

        order_table.grant_read_write_data(ordering_function)
        return ordering_function
