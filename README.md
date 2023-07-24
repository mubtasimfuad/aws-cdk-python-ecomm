# AWS CDK Python Ecommerce Project :rocket:

This repository contains an Ecommerce application built using AWS Cloud Development Kit (CDK) and Python. The application leverages various AWS services to provide functionalities like managing product inventory, processing orders, and handling user interactions.

![Ecommerce Flow](https://user-images.githubusercontent.com/1147445/158019166-96732203-6642-4242-b1d9-d53ece2e1ed3.png)

## Technologies Used

- AWS Cloud Development Kit (CDK)
- Python

## AWS Services Used :package:

The Ecommerce application uses the following AWS services:

- AWS Lambda: For serverless functions to handle backend logic and business processes.
- Amazon DynamoDB: For storing product inventory, order data, and user information.
- Amazon API Gateway: To expose RESTful APIs for users to interact with the application.
- Amazon SQS: For handling asynchronous processing of orders and events.
- Amazon EventBridge (formerly CloudWatch Events): To manage events and triggers for order processing and other application functionalities.

## Getting Started :gear: 

To get started with the project, follow the steps below:

1. Clone the repository to your local machine:

```
git clone https://github.com/mubtasimfuad/aws-cdk-python-ecomm.git
```

2. Install the required dependencies:

Create a virtual environment manually on macOS and Linux:

```bash
$ python3 -m venv .venv
```

After the initialization process completes and the virtual environment is created, you can use the following step to activate your virtual environment.

```bash
$ source .venv/bin/activate
```

For Windows platforms, you would activate the virtual environment like this:

```bash
% .venv\Scripts\activate.bat
```

Once the virtual environment is activated, you can install the required dependencies.

```bash
$ pip install -r requirements.txt
```

3. Configure AWS CLI with your AWS account credentials and default region.

4. Deploy the AWS CDK stacks:

```bash
cd cdk
cdk deploy
```

This will deploy the necessary AWS resources and services required for the Ecommerce application.

## Project Structure

The project is structured as follows:

```
├── app.py
├── cdk
│   ├── backend
│   │   ├── api
│   │   │   ├── infrastructure.py
│   │   ├── cdk_stack.py
│   │   ├── database
│   │   │   ├── infrastructure.py
│   │   ├── eventbus
│   │   │   ├── infrastructure.py
│   │   ├── lambdas
│   │   │   ├── infrastructure.py
│   │   │   └── runtime
│   │   │       ├── basket_microservice.py
│   │   │       ├── client.py
│   │   │       ├── order_microservice.py
│   │   │       └── product_microservice.py
│   │   └── sqs
│   │       ├── infrastructure.py
│   ├── __init__.py
├── cdk.json
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── source.bat
```

- `cdk.json`: Configuration file for AWS CDK.
- `cdk`: Main package containing the application code.
- `backend`: Contains modules for backend services like API, database, lambdas, and queues.

## Functionality

The Ecommerce application provides the following functionality:

1. **Product Inventory Management**: Manage the inventory of products available for purchase.
2. **Order Processing**: Process and fulfill customer orders.
3. **User Interactions**: Allow users to browse products and place orders.

## Contributing

Contributions to the project are welcome! Feel free to raise issues or submit pull requests for improvements, bug fixes, or additional features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You can now begin exploring the source code contained in the `cdk` directory. There is also a very trivial test included that can be run like this:



## Useful commands :white_check_mark: 

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation