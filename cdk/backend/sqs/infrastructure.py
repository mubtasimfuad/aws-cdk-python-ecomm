import aws_cdk as cdk
from constructs import Construct


class eShadhinSQSQueue(Construct):
    def __init__(self, scope: Construct, id: str, lambdas) -> None:
        super().__init__(scope, id)
        # ADD order queue
        self.order_queue = self.create_order_queue()
        # Add the SqsEventSource to the consumer Lambda function
        lambdas.order_lambda.add_event_source(
            cdk.aws_lambda_event_sources.SqsEventSource(
                self.order_queue,
                batch_size=10,
            )
        ) 

    def create_order_queue(self):
        queue = cdk.aws_sqs.Queue(
            self,
            "OrderQueue",
            queue_name="OrderQueue",
            visibility_timeout=cdk.Duration.seconds(30),
        )
        return queue
