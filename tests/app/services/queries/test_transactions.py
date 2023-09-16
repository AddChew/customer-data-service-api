import pytest

from app.deployment import setup_app
from fastapi.testclient import TestClient
from conftest import date_string, query_builder


class TestTransactions:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.client = TestClient(setup_app())
        self.headers = {"accessKey": "test"}
        self.route = "/graphql"
        self.query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "cif", "value": '"0"'}, {"name": "accNum", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )

    def test_missing_access_key(self):
        """
        Test missing access key in request headers.
        """
        response = self.client.get(self.route, params = {"query": self.query})
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    def test_invalid_access_key(self):
        """
        Test invalid access key in request headers.
        """
        response = self.client.get(self.route, headers = {"accessKey": "invalid"}, params = {"query": self.query})
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    def test_missing_query_params(self):
        """
        Test missing query parameters.
        """
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 400
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing refId, cif and/or accNum in query parameters."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    def test_invalid_query_params(self):
        """
        Test invalid query parameters.
        """
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "transactionType", "value": '"invalid"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 400
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Invalid transaction_type in query params. transaction_type takes on the value 'credit', 'debit' or null."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    @pytest.mark.asyncio
    async def test_query_by_refId(self, mock_mongo):
        """
        Test query by refId.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"100"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    @pytest.mark.asyncio
    async def test_query_by_cif(self, mock_mongo):
        """
        Test query by cif.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"0"'}, {"name": "transactionType", "value": '"credit"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"0"'}, {"name": "transactionType", "value": '"debit"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"100"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Customer does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    @pytest.mark.asyncio
    async def test_query_by_accNum(self, mock_mongo):
        """
        Test query by accNum.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "accNum", "value": '"0"'}, {"name": "transactionType", "value": '"credit"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "accNum", "value": '"0"'}, {"name": "transactionType", "value": '"debit"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "accNum", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "accNum", "value": '"100"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

    @pytest.mark.asyncio
    async def test_query_by_refId_cif(self, mock_mongo):
        """
        Test query by refId and cif.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "cif", "value": '"2"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "cif", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

    @pytest.mark.asyncio
    async def test_query_by_refId_accNum(self, mock_mongo):
        """
        Test query by refId and accNum.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "accNum", "value": '"2"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "refId", "value": '"0"'}, {"name": "accNum", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

    @pytest.mark.asyncio
    async def test_query_by_cif_accNum(self, mock_mongo):
        """
        Test query by cif and accNum.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"2"'}, {"name": "accNum", "value": '"2"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [{"name": "cif", "value": '"0"'}, {"name": "accNum", "value": '"0"'}],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]

    @pytest.mark.asyncio
    async def test_query_by_refId_cif_accNum(self, mock_mongo):
        """
        Test query by refId, cif and accNum.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveTransactions",
            arguments = [
                {"name": "refId", "value": '"0"'}, {"name": "cif", "value": '"1"'}, 
                {"name": "accNum", "value": '"1"'}, {"name": "transactionType", "value": '"debit"'}
            ],
            fields = ["refId", "amount", "currency", "fromAccNum", "fromCif", "toAccNum", "toCif", "transDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Transaction does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveTransactions"]

        response = self.client.get(self.route, headers = self.headers, params = {"query": self.query})
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["data"]["retrieveTransactions"] == [dict(
            refId = "0",
            fromCif = "0",
            fromAccNum = "0",
            toCif = "1",
            toAccNum = "1",
            amount = 1000.00,
            currency = "USD",
            transDate = date_string,
        )]