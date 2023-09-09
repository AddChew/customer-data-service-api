import mongomock as mock
from app.schemas import Customer, Account, Transaction
from app.database.fixtures import generate_customers_fixture, generate_accounts_fixture, generate_transactions_fixture, load_fixture


class TestFixtures:

    def setup_method(self):
        self.customers_dicts = generate_customers_fixture()
        self.accounts_dicts = generate_accounts_fixture(self.customers_dicts)
        self.transactions_dicts = generate_transactions_fixture(self.accounts_dicts)

    def test_generate_customers_fixture(self):
        """
        Test generate_customers_fixture function.
        """
        assert len(self.customers_dicts) == 10
        assert all(isinstance(customer, dict) for customer in self.customers_dicts)
        assert all(isinstance(Customer(_id = 'id', **customer), Customer) for customer in self.customers_dicts)

    def test_generate_accounts_fixture(self):
        """
        Test generate_accounts_fixture function.
        """
        assert len(self.accounts_dicts) == 30
        assert all(isinstance(account, dict) for account in self.accounts_dicts)
        assert all(isinstance(Account(_id = 'id', **account), Account) for account in self.accounts_dicts)

    def test_generate_transactions_fixture(self):
        """
        Test generate_transactions_fixture function.
        """
        assert len(self.transactions_dicts) == 100
        assert all(isinstance(transaction, dict) for transaction in self.transactions_dicts)
        assert all(isinstance(Transaction(_id = 'id', **transaction), Transaction) for transaction in self.transactions_dicts)

    def test_load_fixture(self):
        collection_name = "test_collection"
        database = mock.MongoClient().get_database("test_database")
        data = [{"name": f"record {i}"} for i in range(100)]

        load_fixture(database, collection_name, data)
        assert collection_name in database.list_collection_names()
        assert [doc for doc in database[collection_name].find()] == data