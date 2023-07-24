import os
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_iam as iam

# import iam


class eShadhinApi(Construct):
    def __init__(self, scope: Construct, id: str, lambdas) -> None:
        super().__init__(scope, id)
        self.product_api = self.create_product_api(lambdas)
        self.basket_api = self.create_basket_api(lambdas)
        self.order_api = self.create_order_api(lambdas)

    def create_product_api(self, lambdas):
        product_api = cdk.aws_apigateway.LambdaRestApi(
            self,
            "ProductApi",
            handler=lambdas,
            proxy=False,
            rest_api_name="Product Service",
            description="This service serves product.",
        )
        # add resource
        product = product_api.root.add_resource("product")
        product.add_method("GET")
        product.add_method("POST")
        # add resource
        single_product = product.add_resource("{id}")
        single_product.add_method("GET")
        single_product.add_method("PUT")
        single_product.add_method("DELETE")

        return product_api

    def create_basket_api(self, lambdas):
        basket_api = cdk.aws_apigateway.LambdaRestApi(
            self,
            "BasketApi",
            handler=lambdas,
            proxy=False,
            rest_api_name="Basket Service",
            description="This service serves basket.",
        )

        basket = basket_api.root.add_resource("basket")
        basket.add_method("GET")
        basket.add_method("POST")

        single_basket = basket.add_resource("{userName}")
        single_basket.add_method("GET")
        single_basket.add_method("DELETE")

        basket_checkout = basket.add_resource("checkout")
        basket_checkout.add_method("POST")

        return basket_api

    def create_order_api(self, lambdas):
        order_api = cdk.aws_apigateway.LambdaRestApi(
            self,
            "OrderApi",
            handler=lambdas,
            proxy=False,
            rest_api_name="Order Service",
            description="This service serves order.",
        )
        # add resource
        order = order_api.root.add_resource("order")
        order.add_method("GET")

        single_order = order.add_resource("{userName}")
        single_order.add_method("GET")

        return order_api
