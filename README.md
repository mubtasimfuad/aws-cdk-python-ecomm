# AWS CDK Python Ecommerce Project

This repository contains an Ecommerce application built using AWS Cloud Development Kit (CDK) and Python. The application leverages various AWS services to provide functionalities like managing product inventory, processing orders, and handling user interactions.

## Getting Started

To get started with the project, follow the steps below:

1. Clone the repository to your local machine:

```
git clone https://github.com/your-username/aws-cdk-python-ecomm.git
```

2. Install the required dependencies:

manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```


3. Configure AWS CLI with your AWS account credentials and default region.

4. Deploy the AWS CDK stacks:

```
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
│   │   │   └── __pycache__
│   │   │       └── infrastructure.cpython-310.pyc
│   │   ├── cdk_stack.py
│   │   ├── database
│   │   │   ├── infrastructure.py
│   │   │   
│   │   ├── eventbus
│   │   │   ├── infrastructure.py
│   │   │   
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

- `cdk.json`: Configuration file for AWS CDK.
- `ecomm`: Main package containing the application code.
- `backend`: Contains modules for backend services like API, database, lambdas, and queues.

## Functionality

The Ecommerce application provides the following functionality:

1. **Product Inventory Management**: Manage the inventory of products available for purchase.
2. **Order Processing**: Process and fulfill customer orders.
3. **User Interactions**: Allow users to browse products and place orders.

## Contributing

Contributions to the project are welcome! Feel free to raise issues or submit pull requests for improvements, bug fixes, or additional features.

## License


T

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

