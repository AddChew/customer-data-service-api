import os
from urllib.parse import quote_plus


mongo_host = os.getenv("MONGO_HOST", "mongo")
mongo_username = quote_plus(os.getenv("MONGO_INITDB_ROOT_USERNAME", "mongo")) 
mongo_password = quote_plus(os.getenv("MONGO_INITDB_ROOT_PASSWORD", "mongo"))
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}/"

customers_database = os.getenv("CUSTOMERS_DATABASE", "customers_data")

customers_collection = os.getenv("CUSTOMERS_COLLECTION", "customers")
accounts_collection = os.getenv("ACCOUNTS_COLLECTION", "accounts")
transactions_collection = os.getenv("TRANSACTIONS_COLLECTION", "transactions")