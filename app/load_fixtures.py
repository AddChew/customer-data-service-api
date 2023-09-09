from database import settings
from pymongo import MongoClient
from database.fixtures import generate_customers_fixture, generate_accounts_fixture, generate_transactions_fixture, load_fixture


client = MongoClient(settings.mongo_uri)
database = client.get_database(settings.customers_database)

customers = generate_customers_fixture()
accounts = generate_accounts_fixture(customers)
transactions = generate_transactions_fixture(accounts)


load_fixture(
    database = database,
    collection_name = settings.customers_collection, 
    data = customers
)

load_fixture(
    database = database,
    collection_name = settings.accounts_collection, 
    data = accounts
)

load_fixture(
    database = database,
    collection_name = settings.transactions_collection, 
    data = transactions
)