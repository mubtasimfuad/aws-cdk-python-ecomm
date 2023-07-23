import os
import aws_cdk as cdk
import pathlib
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
class eShadhinApi(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        product_lambda = lambda_.Function(
            self,
            "ProductLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler = "product_microservice.lambda_handler",
            code=lambda_.Code.from_asset(
                os.path.join(current_dir, "runtime")
            ),
            timeout=cdk.Duration.seconds(10),
            memory_size=128
        )
        product_api = cdk.aws_apigateway.LambdaRestApi(
            self,
            "ProductApi",
            handler=product_lambda,
            proxy=False,
            rest_api_name="Product Service",
            description="This service serves product."
        )
        #add resource
        product_resource = product_api.root.add_resource("product")
        product_resource.add_method("GET")
        product_resource.add_method("POST")
        product_resource.add_method("PUT")
        product_resource.add_method("DELETE")
        #add resource
        product_id_resource = product_resource.add_resource("{id}")
        product_id_resource.add_method("GET")
        product_id_resource.add_method("POST")
        product_id_resource.add_method("PUT")
        product_id_resource.add_method("DELETE")
        
