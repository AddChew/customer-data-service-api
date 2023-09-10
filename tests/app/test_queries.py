import pytest
import datetime

from app.deployment import setup_app
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from graphql_query import Argument, Operation, Query


class TestQuery:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        app = setup_app()
        self.client = TestClient(app)
        self.graphql_route = "/graphql"
        self.headers = {"accessKey": "test"}

        date = datetime.date(2023, 9, 10)
        time = datetime.datetime.min.time()
        self.date = datetime.datetime.combine(date, time)
        self.date_string = self.date.strftime("%Y-%m-%dT%H:%M:%S")

        client = AsyncMongoMockClient()
        database = client.get_database("customers_data")

        self.customers_collection = database.get_collection("customers")
        self.accounts_collection = database.get_collection("accounts")
        self.transactions_collection = database.get_collection("transactions")

        cif = Argument(name = "cif", value = '"0"')
        getCustomer = Query(
            name = "getCustomer",
            arguments = [cif],
            fields = [
                "cif",
                "name",
                "dateOfBirth",
                "address",
                "nationality",
                "joinDate",
            ]
        )
        operation = Operation(name = "Query", type = "query", queries = [getCustomer])
        self.getCustomerQuery = operation.render()

    def test_missing_access_key(self):
        """
        Test missing access key in request headers.
        """
        response = self.client.get(
            self.graphql_route,
            params = {"query": self.getCustomerQuery}
        )
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["getCustomer"]

    def test_invalid_access_key(self):
        """
        Test invalid access key in request headers.
        """
        response = self.client.get(
            self.graphql_route,
            params = {"query": self.getCustomerQuery},
            headers = {"accessKey": "invalid"},
        )
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["getCustomer"]

    @pytest.mark.asyncio
    async def test_getCustomer_exists(self, monkeypatch):
        """
        Test getCustomer method where queried customer exists.
        """
        customers_dicts = [
            {
                "cif": f"{i}",
                "name": f"name {i}",
                "dateOfBirth": self.date,
                "address": f"address {i}",
                "nationality": f"nationality {i}",
                "joinDate": self.date
            }
            for i in range(11)
        ]
        await self.customers_collection.insert_many(customers_dicts)
        monkeypatch.setattr("app.queries.customers_collection", self.customers_collection)

        response = self.client.get(
            self.graphql_route,
            params = {"query": self.getCustomerQuery},
            headers = self.headers,
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["getCustomer"] == {
            "cif": "0",
            "name": "name 0",
            "dateOfBirth": self.date_string,
            "address": "address 0",
            "nationality": "nationality 0",
            "joinDate": self.date_string
        }

    @pytest.mark.asyncio
    async def test_getCustomer_does_not_exist(self, monkeypatch):
        """
        Test getCustomer method where queried customer does not exist.
        """
        cif = Argument(name = "cif", value = '"11"')
        getCustomer = Query(
            name = "getCustomer",
            arguments = [cif],
            fields = [
                "cif",
                "name",
                "dateOfBirth",
                "address",
                "nationality",
                "joinDate",
            ]
        )
        operation = Operation(name = "Query", type = "query", queries = [getCustomer])
        query = operation.render()
        monkeypatch.setattr("app.queries.customers_collection", self.customers_collection)

        response = self.client.get(
            self.graphql_route,
            params = {"query": query},
            headers = self.headers,
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Customer does not exist"
        assert json_response["errors"][0]["path"] == ["getCustomer"]

    @pytest.mark.asyncio
    async def test_getAccount_exists(self, monkeypatch):
        """
        Test getAccount method where queried account exists.
        """
        accounts_dicts = [
            dict(
                accNum = f"{i}",
                accHolderCif = f"{i}",
                accHolderName = f"name {i}",
                accType = f"accType {i}",
                currency = f"currency {i}",
                createDate = self.date,
                accStatus = f"accStatus {i}",
            )
            for i in range(10)
        ]
        await self.accounts_collection.insert_many(accounts_dicts)
        monkeypatch.setattr("app.queries.accounts_collection", self.accounts_collection)

        accNum = Argument(name = "accNum", value = '"0"')
        getAccount = Query(
            name = "getAccount",
            arguments = [accNum],
            fields = [
                "accHolderCif",
                "accHolderName",
                "accNum",
                "accStatus",
                "accType",
                "createDate",
                "currency"
            ]
        )
        operation = Operation(name = "Query", type = "query", queries = [getAccount])
        query = operation.render()

        response = self.client.get(
            self.graphql_route,
            params = {"query": query},
            headers = self.headers,
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["getAccount"] == {
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": self.date_string,
            "currency": "currency 0"
        }

    @pytest.mark.asyncio
    async def test_getAccount_does_not_exist(self, monkeypatch):
        """
        Test getAccount method where queried account does not exist.
        """
        monkeypatch.setattr("app.queries.accounts_collection", self.accounts_collection)

        accNum = Argument(name = "accNum", value = '"10"')
        getAccount = Query(
            name = "getAccount",
            arguments = [accNum],
            fields = [
                "accHolderCif",
                "accHolderName",
                "accNum",
                "accStatus",
                "accType",
                "createDate",
                "currency"
            ]
        )
        operation = Operation(name = "Query", type = "query", queries = [getAccount])
        query = operation.render()

        response = self.client.get(
            self.graphql_route,
            params = {"query": query},
            headers = self.headers,
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist"
        assert json_response["errors"][0]["path"] == ["getAccount"]
   
    # @field(permission_classes = permission_classes)
    # async def getTransaction(refId: str) -> Transaction:
    #     """
    #     Retrieve transaction details based on reference id.

    #     Args:
    #         refId (str): Transaction reference id to retrieve information on.

    #     Raises:
    #         Exception: Raised when transaction does not exist.

    #     Returns:
    #         Transaction: Transaction object.
    #     """
    #     transaction = await transactions_collection.find_one({"refId": refId})
    #     if transaction:
    #         return Transaction(**transaction)
    #     raise Exception("Transaction does not exist")
    
    # @field(permission_classes = permission_classes)
    # async def getAccounts(cif: str) -> List[Account]:
    #     """
    #     Retrieve list of accounts belonging to a customer.

    #     Args:
    #         cif (str): Cif of customer to retrieve accounts for.

    #     Returns:
    #         List[Account]: List of Account objects.
    #     """
    #     await check_customer_exists(cif)
    #     accounts = accounts_collection.find({"accHolderCif": cif})
    #     return [Account(**account) async for account in accounts]    
    
    # @field(permission_classes = permission_classes)
    # async def getTransactionsByCif(cif: str, transaction_type: Optional[str] = None) -> List[Transaction]:
    #     """
    #     Retrieve transactions by customer cif.

    #     Args:
    #         cif (str): Cif of customer to retrieve transactions for.
    #         transaction_type (Optional[str], optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

    #     Returns:
    #         List[Transaction]: List of Transaction objects.
    #     """
    #     check_transaction_type(transaction_type)
    #     await check_customer_exists(cif)

    #     if transaction_type == "credit":
    #         filters = {"toCif": cif}
            
    #     elif transaction_type == "debit":
    #         filters = {"fromCif": cif}

    #     else:
    #         filters = {
    #             "$or": [
    #                 {"fromCif": { "$eq": cif }}, 
    #                 {"toCif": { "$eq": cif }},
    #             ]
    #         }
    #     return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]

    # @field(permission_classes = permission_classes)
    # async def getTransactionsByAccNum(accNum: str, transaction_type: Optional[str] = None) -> List[Transaction]:
    #     """
    #     Retrieve transactions by account number.

    #     Args:
    #         accNum (str): Account number to retrieve transactions on.
    #         transaction_type (Optional[str], optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

    #     Returns:
    #         List[Transaction]: List of Transaction objects.
    #     """
    #     check_transaction_type(transaction_type)
    #     await check_account_exists(accNum)

    #     if transaction_type == "credit":
    #         filters = {"toAccNum": accNum}
            
    #     elif transaction_type == "debit":
    #         filters = {"fromAccNum": accNum}

    #     else:
    #         filters = { 
    #             "$or": [
    #                 {"fromAccNum": { "$eq": accNum }}, 
    #                 {"toAccNum": { "$eq": accNum }},
    #             ]
    #         }
    #     return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]