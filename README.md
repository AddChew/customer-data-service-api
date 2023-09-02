# Customer Data Service API

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

4. Copy and paste the generated access key into the .env file as shown below:
```
ACCESS_KEY=<your generated access key>
```

5. Add the following key-value pairs into the .env file as shown below:
```
MONGO_INITDB_ROOT_USERNAME=<your mongodb username>
MONGO_INITDB_ROOT_PASSWORD=<your mongodb password>
```

6. Spin up containers
```
docker compose build
```

7. Execute the following terminal command
```shell
cd ..
serve run app.main:deployment
```