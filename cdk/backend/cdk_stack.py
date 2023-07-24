from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from cdk.backend.database.infrastructure import eShadhinDatabase
from cdk.backend.api.infrastructure import eShadhinApi
from cdk.backend.lambdas.infrastructure import eShadhinLambda


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        database = eShadhinDatabase(self, "eShadhinDatabase")

        lambdas = eShadhinLambda(self, "eShadhinLambda", db=database)

        product_apigw = eShadhinApi(self, "eShadhinApi", lambdas=lambdas.product_lambda)
        # ad environment variable to lambda
        lambdas.product_lambda.add_environment(
            "PRODUCT_TABLE_NAME", database.product_table.table_name
        )
