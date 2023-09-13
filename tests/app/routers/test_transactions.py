import pytest

from app.deployment import app
from conftest import date_string
from fastapi.testclient import TestClient


class TestTransactions:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.client = TestClient(app)
        self.headers = {"accessKey": "test"}
        self.route = "/transactions"

    def test_missing_access_key(self):
        """
        Test missing access key in request headers.
        """
        response = self.client.get(self.route)
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["detail"] == "Missing or invalid access key in request headers"

    def test_invalid_access_key(self):
        """
        Test invalid access key in request headers.
        """
        response = self.client.get(self.route, headers = {"accessKey": "invalid"})
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["detail"] == "Missing or invalid access key in request headers"

    def test_missing_query_params(self):
        """
        Test missing query parameters.
        """
        response = self.client.get(self.route, headers = self.headers)
        assert response.status_code == 400
        
        json_response = response.json()
        assert json_response["detail"] == "Missing refId, cif and/or accNum in query parameters."

    def test_invalid_query_params(self):
        """
        Test invalid query parameters.
        """
        response = self.client.get(self.route, headers = self.headers, params = {"refId": "0", "transaction_type": "invalid"})
        assert response.status_code == 400
        
        json_response = response.json()
        assert json_response["detail"] == "Invalid transaction_type in query params. transaction_type takes on the value 'credit', 'debit' or null."

    @pytest.mark.asyncio
    async def test_query_by_refId(self, mock_mongo):
        """
        Test query by refId.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"refId": "0"})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        response = self.client.get(self.route, headers = self.headers, params = {"refId": "100"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Transaction does not exist."

# async def retrieve_transactions(refId: str = None, cif: str = None, accNum: str = None, transaction_type: str = None) -> List[Transaction]:
#     """
#     Retrieve list of transactions by refId, cif, accNum and transaction_type.

#     Args:
#         refId (str, optional): Transaction reference id of transaction to retrieve. Defaults to None.
#         cif (str, optional): Cif of customer to retrieve transactions for. Defaults to None.
#         accNum (str, optional): Account number of customer to retrieve transactions for. Defaults to None.
#         transaction_type (str, optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

#     Raises:
#         HTTPException: Raised when transaction does not exist.

#     Returns:
#         List[Transaction]: List of Transaction objects.
#     """
#     prefix_map = {
#         "credit": "to",
#         "debit": "from",
#         None: ("to", "from"), 
#     }
#     prefix = prefix_map[transaction_type]

#     filters = {}
#     if cif:
#         await retrieve_customer(cif)
#         if isinstance(prefix, tuple):
#             filters["$or"] = [{f"{p}Cif": {"$eq": cif}} for p in prefix]
#         else:
#             filters[f"{prefix}Cif"] = cif

#     if accNum:
#         await retrieve_accounts(cif, accNum)
#         if isinstance(prefix, tuple):
#             filters["$or"] = [{f"{p}AccNum": {"$eq": accNum}} for p in prefix]
#         else:
#             filters[f"{prefix}AccNum"] = accNum

#     if refId:
#         filters["refId"] = refId

#     transactions = [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]
#     if transactions:
#         return transactions
#     raise HTTPException(
#         status_code = status.HTTP_404_NOT_FOUND,
#         detail = "Transaction does not exist",
#     )

#     @pytest.mark.asyncio
#     async def test_getTransactionsByCif_customer_does_not_exist(self, mock_mongo):
#         """
#         Test getTransactionsByCif method where queried customer does not exist.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"11"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"] is None
#         assert json_response["errors"][0]["message"] == "Customer does not exist"
#         assert json_response["errors"][0]["path"] == ["getTransactionsByCif"]

#     @pytest.mark.asyncio
#     async def test_getTransactionsByCif_exist_credit(self, mock_mongo):
#         """
#         Test getTransactionsByCif method for credit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"1"'}, {"name": "transactionType", "value": '"credit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"0"'}, {"name": "transactionType", "value": '"credit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == []

#     @pytest.mark.asyncio
#     async def test_getTransactionsByCif_exist_debit(self, mock_mongo):
#         """
#         Test getTransactionsByCif method for debit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"0"'}, {"name": "transactionType", "value": '"debit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"1"'}, {"name": "transactionType", "value": '"debit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == []

#     @pytest.mark.asyncio
#     async def test_getTransactionsByCif_exist_credit_debit(self, mock_mongo):
#         """
#         Test getTransactionsByCif method for both credit and debit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"0"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"2"'}, {"name": "transactionType", "value": "null"}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByCif"] == []

#     @pytest.mark.asyncio
#     async def test_getTransactionsByAccNum_customer_does_not_exist(self, mock_mongo):
#         """
#         Test getTransactionsByAccNum method where queried customer does not exist.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"11"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"] is None
#         assert json_response["errors"][0]["message"] == "Account does not exist"
#         assert json_response["errors"][0]["path"] == ["getTransactionsByAccNum"]

#     @pytest.mark.asyncio
#     async def test_getTransactionsByAccNum_exist_credit(self, mock_mongo):
#         """
#         Test getTransactionsByAccNum method for credit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"1"'}, {"name": "transactionType", "value": '"credit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"0"'}, {"name": "transactionType", "value": '"credit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == []

#     @pytest.mark.asyncio
#     async def test_getTransactionsByAccNum_exist_debit(self, mock_mongo):
#         """
#         Test getTransactionsByAccNum method for debit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"0"'}, {"name": "transactionType", "value": '"debit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"1"'}, {"name": "transactionType", "value": '"debit"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == []

#     @pytest.mark.asyncio
#     async def test_getTransactionsByAccNum_exist_credit_debit(self, mock_mongo):
#         """
#         Test getTransactionsByAccNum method for both credit and debit transactions.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"0"'}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == [dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )]

#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"2"'}, {"name": "transactionType", "value": "null"}],
#             fields = [
#                 "refId",
#                 "amount",
#                 "currency",
#                 "fromAccNum",
#                 "fromCif",
#                 "toAccNum",
#                 "toCif",
#                 "transDate",      
#             ]
#         )
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": query},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getTransactionsByAccNum"] == []