import os
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_iam as iam
#import iam

class eShadhinApi(Construct):
    def __init__(self, scope: Construct, id: str, lambdas) -> None:
        super().__init__(scope, id)

        product_api = cdk.aws_apigateway.LambdaRestApi(
            self,
            "ProductApi",
            handler=lambdas,
            proxy=False,
            rest_api_name="Product Service",
            description="This service serves product.",
            
        )
        #add resource
        product_resource = product_api.root.add_resource("product")
        product_resource.add_method("GET")
        product_resource.add_method("POST")
        #add resource
        product_id_resource = product_resource.add_resource("{id}")
        product_id_resource.add_method("GET")
        product_id_resource.add_method("PUT")
        product_id_resource.add_method("DELETE")

    