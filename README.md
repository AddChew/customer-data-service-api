[![Unit Tests](https://github.com/AddChew/customer-data-service-api/actions/workflows/tests.yml/badge.svg?branch=graphql-mongodb)](https://github.com/AddChew/customer-data-service-api/actions/workflows/tests.yml)

# Customer Data Service API

GraphQL API for customers, accounts and transactions data. 

Built with:
* MongoDB
* Motor
* FastAPI
* Ray Serve
* Strawberry

## Project Setup

1. Navigate into the deploy folder from the project root folder (i.e. customer-data-service-api/deploy)
```shell
cd deploy
```

2. Create a .env file with the following terminal command
```shell
touch .env
```

3. Generate an access key with the following terminal command
```sh
openssl rand -hex 16
```

4. Add the following key-value pairs into the .env file
```
NUM_REPLICAS=2

APP_PORT=8000
RAY_DASHBOARD_PORT=8265

FIXTURES_SEED=0
NUM_CUSTOMERS=100
NUM_ACCOUNTS=300
NUM_TRANSACTIONS=5000

MONGO_HOST=mongo
MONGO_INITDB_ROOT_USERNAME=<your mongodb username>
MONGO_INITDB_ROOT_PASSWORD=<your mongodb password>

CUSTOMERS_DATABASE=customers_data

CUSTOMERS_COLLECTION=customers
ACCOUNTS_COLLECTION=accounts
TRANSACTIONS_COLLECTION=transactions

ACCESS_KEY=<your generated access key>
```

5. Build docker image and start containers
```shell
docker compose up -d --build
```

6. Navigate to the following urls to access the respective services

| URL                              | Service       |
| -------------------------------- |-------------- |
| http://localhost:8000/graphql    | GraphiQL      |
| http://localhost:8000/docs       | SwaggerUI     |
| http://localhost:8000/redoc      | Redoc         |
| http://localhost:8265/#/overview | Ray dashboard |

## How To Run Unittests

1. Navigate to project root folder (i.e. customer-data-service-api) 

2. Install the necessary dependencies
```shell
pip install -r requirements-dev.txt
```

3. Execute unittests
```shell
coverage run -m pytest -v
```

4. Check test coverage
```shell
coverage report -m --fail-under=95
```
