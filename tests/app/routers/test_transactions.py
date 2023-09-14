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

    @pytest.mark.asyncio
    async def test_query_by_cif(self, mock_mongo):
        """
        Test query by cif.
        """
        await mock_mongo

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0", "transaction_type": "credit"})
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["detail"] == "Transaction does not exist."

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0", "transaction_type": "debit"})
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

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0"})
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

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "100"})
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["detail"] == "Customer does not exist."

    @pytest.mark.asyncio
    async def test_query_by_accNum(self, mock_mongo):
        """
        Test query by accNum.
        """
        await mock_mongo

        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "0", "transaction_type": "credit"})
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["detail"] == "Transaction does not exist."

        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "0", "transaction_type": "debit"})
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

        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "0"})
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

        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "100"})
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["detail"] == "Account does not exist."