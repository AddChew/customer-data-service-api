# Customer Data Service API

## Project Setup

1. Navigate into the project root folder (i.e. customer-data-service-api)

2. Create a .env file with the following terminal command
```shell
touch .env
```

3. Generate an access key with the following terminal command
```sh
openssl rand -hex 16
```

4. Copy and paste the generated access key into the .env file as shown below:
```python
# .env
ACCESS_KEY=<your generated access key>
```

5. Execute the following terminal command
```
serve run app.main:deployment
```