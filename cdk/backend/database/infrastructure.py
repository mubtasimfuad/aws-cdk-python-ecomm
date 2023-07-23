import builtins
import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct



class eShadhinDatabase(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
        # product table
        self.product_table = self.create_product_table()
    
    def create_product_table(self):
        table = dynamodb.Table(
            self,
            "ProductTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        return table