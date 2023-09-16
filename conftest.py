import pytest
import datetime

from typing import List, Dict
from mongomock_motor import AsyncMongoMockClient
from graphql_query import Argument, Operation, Query


date = datetime.datetime.combine(datetime.date(2023, 9, 10), datetime.datetime.min.time())
date_string = date.strftime("%Y-%m-%d")


@pytest.fixture
async def mock_mongo(monkeypatch):
    """
    Fixture to monkeypatch mongo collections.
    """
    client = AsyncMongoMockClient()
    database = client.get_database("customers_data")

    customers_collection = database.get_collection("customers")
    accounts_collection = database.get_collection("accounts")
    transactions_collection = database.get_collection("transactions")

    customers_dicts = [
        {
            "cif": f"{i}",
            "name": f"name {i}",
            "dateOfBirth": date,
            "address": f"address {i}",
            "nationality": f"nationality {i}",
            "joinDate": date
        }
        for i in range(11)
    ]
    await customers_collection.insert_many(customers_dicts)
    monkeypatch.setattr("app.services.queries.customers.customers_collection", customers_collection)

    accounts_dicts = [
        dict(
            accNum = f"{i}",
            accHolderCif = f"{i}",
            accHolderName = f"name {i}",
            accType = f"accType {i}",
            currency = f"currency {i}",
            createDate = date,
            accStatus = f"accStatus {i}",
        )
        for i in range(10)
    ]
    await accounts_collection.insert_many(accounts_dicts)
    monkeypatch.setattr("app.services.queries.accounts.accounts_collection", accounts_collection)

    transactions_dicts = [
        dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date
        ),
    ]
    await transactions_collection.insert_many(transactions_dicts)
    monkeypatch.setattr("app.services.queries.transactions.transactions_collection", transactions_collection)


def query_builder(query_name: str, arguments: List[Dict], fields: list) -> str:
    """
    Generate GraphQL query string.

    Args:
        query_name (str): Name of query.
        arguments (List[Dict]): List of arguments, with each argument being a dictionary with 
            the format: {"name": <name>, "value": <value>}.
        fields (list): Fields to include in query response.

    Returns:
        str: GraphQL query string.
    """
    arguments = [Argument(**argument) for argument in arguments]
    query = Query(
        name = query_name,
        arguments = arguments,
        fields = fields
    )
    operation = Operation(name = "Query", type = "query", queries = [query])
    return operation.render()