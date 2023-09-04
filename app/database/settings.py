import os
from urllib.parse import quote_plus

# TODO: remove all the defaults
mongo_username = quote_plus(os.getenv("MONGO_INITDB_ROOT_USERNAME", "mongo")) 
mongo_password = quote_plus(os.getenv("MONGO_INITDB_ROOT_PASSWORD", "mongo"))
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"

customers_database = os.getenv("CUSTOMERS_DATABASE", "customers_data")

customers_collection = os.getenv("CUSTOMERS_COLLECTION", "customers")
accounts_collection = os.getenv("ACCOUNTS_COLLECTION", "accounts")
transactions_collection = os.getenv("TRANSACTIONS_COLLECTION", "transactions")