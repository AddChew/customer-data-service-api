import os
import re
from faker import Faker
from datetime import datetime
from typing import List, Dict
from faker.providers import DynamicProvider


seed = int(os.getenv('FIXTURES_SEED', 0))
num_customers = int(os.getenv('NUM_CUSTOMERS', 10))
num_accounts = int(os.getenv('NUM_ACCOUNTS', 30))
num_transactions = int(os.getenv('NUM_TRANSACTIONS', 100))

Faker.seed(seed)
fake = Faker()
time = datetime.min.time()


def generate_customers_fixture() -> List[Dict]:
    """
    Randomly generate a list of customers.

    Returns:
        List[Dict]: Randomly generated list of customers.
    """
    customers = []
    for _ in range(num_customers):
        dateOfBirth = fake.date_of_birth(minimum_age = 21, maximum_age = 80)
        joinDate = fake.past_date(dateOfBirth)

        customer = dict(
            cif = fake.unique.bban(),
            name = fake.unique.name(),
            dateOfBirth = datetime.combine(dateOfBirth, time),
            address = fake.unique.address(),
            nationality = fake.country_code(),
            joinDate = datetime.combine(joinDate, time),
        )
        customers.append(customer)
    return customers


def generate_accounts_fixture(customers: list) -> List[Dict]:
    """
    Randomly generate a list of customer accounts.

    Args:
        customers (list): List of customers to generate accounts for.

    Returns:
        List[Dict]: Randomly generated list of customer accounts.
    """
    accounts = []

    customer_provider = DynamicProvider(
        provider_name = "customer",
        elements = customers,
    )
    status_provider = DynamicProvider(
        provider_name = "status",
        elements = ["Active", "Inactive"],
    )

    fake.add_provider(customer_provider)
    fake.add_provider(status_provider)

    for _ in range(num_accounts):
        customer = fake.customer()
        joinDate = customer.get("joinDate")
        createDate = fake.past_date(joinDate)

        account = dict(
            accNum = fake.unique.credit_card_number(),
            accHolderCif = customer.get("cif"),
            accHolderName = customer.get("name"),
            accType = fake.credit_card_provider(),
            currency = 'USD',
            createDate = datetime.combine(createDate, time),
            accStatus = fake.status()
        )
        accounts.append(account)
    return accounts


def generate_transactions_fixture(accounts: list) -> List[Dict]:
    """
    Randomly generate a list of customer transactions.

    Args:
        accounts (list): List of accounts to generate transactions for.

    Returns:
        List[Dict]: Randomly generated list of transactions.
    """
    transactions = []
    account_provider = DynamicProvider(
        provider_name = "account",
        elements = accounts,
    )
    fake.add_provider(account_provider)

    for _ in range(num_transactions):
        from_account = fake.account()
        to_account = fake.account()
        transDate = fake.past_date(max(from_account.get("createDate"), to_account.get("createDate")))

        transaction = dict(
            refId = fake.unique.ean(),
            fromCif = from_account.get("accHolderCif"),
            fromAccNum = from_account.get("accNum"),
            toCif = to_account.get("accHolderCif"),
            toAccNum = to_account.get("accNum"),
            amount = float(re.sub(r'[$,]', '', fake.pricetag())),
            currency = "USD",
            transDate = datetime.combine(transDate, time)
        )
        transactions.append(transaction)
    return transactions


# TODO: pytest
# TODO: setup github actions