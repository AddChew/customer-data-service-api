from typing import List, Dict
from database import settings
from pymongo import MongoClient
from database.fixtures import generate_customers_fixture, generate_accounts_fixture, generate_transactions_fixture


client = MongoClient(settings.mongo_uri)
database = client.get_database(settings.customers_database)


def load_fixture(collection_name: str, data: List[Dict]):
    database.drop_collection(collection_name)
    collection = database.get_collection(collection_name)
    collection.insert_many(data)


if __name__ == '__main__':

    load_fixture(
        collection_name = settings.customers_collection, 
        data = generate_customers_fixture()
    )

    load_fixture(
        collection_name = settings.accounts_collection, 
        data = generate_accounts_fixture()
    )

    load_fixture(
        collection_name = settings.transactions_collection, 
        data = generate_transactions_fixture()
    )