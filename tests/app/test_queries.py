# class TestQuery:

#     def setup_class(self):
#         """
#         Setup state to be used across tests.
#         """
#         app = setup_app()
#         self.client = TestClient(app)
#         self.graphql_route = "/graphql"
#         self.headers = {"accessKey": "test"}

#         self.getCustomerQuery = query_builder(
#             query_name = "getCustomer",
#             arguments = [{"name": "cif", "value": '"0"'}],
#             fields = [
#                 "cif",
#                 "name",
#                 "dateOfBirth",
#                 "address",
#                 "nationality",
#                 "joinDate",
#             ]
#         )

#     @pytest.mark.asyncio
#     async def test_getCustomer_exists(self, mock_mongo):
#         """
#         Test getCustomer method where queried customer exists.
#         """
#         await mock_mongo
#         response = self.client.get(
#             self.graphql_route,
#             params = {"query": self.getCustomerQuery},
#             headers = self.headers,
#         )
#         assert response.status_code == 200

#         json_response = response.json()
#         assert json_response["data"]["getCustomer"] == {
#             "cif": "0",
#             "name": "name 0",
#             "dateOfBirth": date_string,
#             "address": "address 0",
#             "nationality": "nationality 0",
#             "joinDate": date_string
#         }

#     @pytest.mark.asyncio
#     async def test_getCustomer_does_not_exist(self, mock_mongo):
#         """
#         Test getCustomer method where queried customer does not exist.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getCustomer",
#             arguments = [{"name": "cif", "value": '"11"'}],
#             fields = [
#                 "cif",
#                 "name",
#                 "dateOfBirth",
#                 "address",
#                 "nationality",
#                 "joinDate",
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
#         assert json_response["errors"][0]["path"] == ["getCustomer"]

#     @pytest.mark.asyncio
#     async def test_getTransaction_exists(self, mock_mongo):
#         """
#         Test getTransaction method where queried transaction exists.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransaction",
#             arguments = [{"name": "refId", "value": '"0"'}],
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
#         assert json_response["data"]["getTransaction"] == dict(
#             refId = "0",
#             fromCif = "0",
#             fromAccNum = "0",
#             toCif = "1",
#             toAccNum = "1",
#             amount = 1000.00,
#             currency = "USD",
#             transDate = date_string,
#         )

#     @pytest.mark.asyncio
#     async def test_getTransaction_does_not_exist(self, mock_mongo):
#         """
#         Test getTransaction method where queried transaction does not exist.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransaction",
#             arguments = [{"name": "refId", "value": '"100"'}],
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
#         assert json_response["errors"][0]["message"] == "Transaction does not exist"
#         assert json_response["errors"][0]["path"] == ["getTransaction"]

#     @pytest.mark.asyncio
#     async def test_getTransactions_invalid_transaction_type(self, mock_mongo):
#         """
#         Test invalid transaction type for getTransactionsByCif and getTransactionsByAccNum methods.
#         """
#         await mock_mongo
#         query = query_builder(
#             query_name = "getTransactionsByCif",
#             arguments = [{"name": "cif", "value": '"0"'}, {"name": "transactionType", "value": '"invalid"'}],
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
#         assert json_response["errors"][0]["message"] == "Invalid transaction_type. transaction_type takes on the value 'credit', 'debit' or null."
#         assert json_response["errors"][0]["path"] == ["getTransactionsByCif"]

#         query = query_builder(
#             query_name = "getTransactionsByAccNum",
#             arguments = [{"name": "accNum", "value": '"0"'}, {"name": "transactionType", "value": '"invalid"'}],
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
#         assert json_response["errors"][0]["message"] == "Invalid transaction_type. transaction_type takes on the value 'credit', 'debit' or null."
#         assert json_response["errors"][0]["path"] == ["getTransactionsByAccNum"]

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