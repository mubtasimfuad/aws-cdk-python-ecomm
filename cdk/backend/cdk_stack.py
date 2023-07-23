from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from cdk.backend.database.infrastructure import eShadhinDatabase
from cdk.backend.api.infrastructure import eShadhinApi

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        database = eShadhinDatabase(self, "eShadhinDatabase")
        product_apigw = eShadhinApi(self, "eShadhinApi")
       