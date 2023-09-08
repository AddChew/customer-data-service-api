from typing import List, Dict
from pymongo import MongoClient
from pymongo.database import Database


def load_fixture(database: Database, collection_name: str, data: List[Dict]):
    """
    Load data fixture into collection.

    Args:
        database (Database): Database to load data into.
        collection_name (str): Name of collection to load data into.
        data (List[Dict]): Data to load into collection.
    """
    database.drop_collection(collection_name)
    collection = database.get_collection(collection_name)
    collection.insert_many(data)


if __name__ == '__main__':
    from database import settings
    from database.fixtures import generate_customers_fixture, generate_accounts_fixture, generate_transactions_fixture

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