import os
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_lambda as lambda_




class eShadhinLambda(Construct):
    def __init__(self, scope: Construct, id: str,db) -> None:
        super().__init__(scope, id)
        self.product_lambda = self.create_product_lambda(db) 
        #get db value

    def create_product_lambda(self,db):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        product_lambda= lambda_.Function(
            self,
            "ProductLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="product_microservice.lambda_handler",
            code=lambda_.Code.from_asset(
                os.path.join(current_dir, "runtime")
            ),
            memory_size=128,
            
            )
        #add permission to lambda
        
        db.product_table.grant_read_write_data(product_lambda)
        return product_lambda