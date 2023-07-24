import aws_cdk as cdk
from constructs import Construct


class eShadhinEventBus(Construct):
    # Create the event bus
    def __init__(self, scope: Construct, id: str, queue, lambdas) -> None:
        super().__init__(scope, id)
        self.event_bus = self.create_event_bus()
        # Create the rule for CheckoutBasket events
        self.checkout_basket_rule = self.create_rule_for_checkout_basket()
        # need to pass target SQS queue
        self.checkout_basket_rule.add_target(
            cdk.aws_events_targets.SqsQueue(queue=queue.order_queue)
        )
        # Grant permission to publish events to the event bus
        self.event_bus.grant_put_events_to(lambdas.basket_lambda)

        # create event bus function

    def create_event_bus(self):
        event_bus = cdk.aws_events.EventBus(
            self,
            "eShadhinEventBus",
            event_bus_name="eShadhinEventBus",
        )
        return event_bus

    def create_rule_for_checkout_basket(self):
        rule = cdk.aws_events.Rule(
            self,
            "CheckoutBasketRule",
            description="CheckoutBasketRule",
            event_bus=self.event_bus,
            enabled=True,
            event_pattern=cdk.aws_events.EventPattern(
                source=["com.shadhin.basket.checkoutbasket"],
                detail_type=["CheckoutBasket"],
            ),
            rule_name="CheckoutBasketRule",
        )
        return rule
