import pytest

from app.deployment import app
from conftest import date_string
from fastapi.testclient import TestClient


class TestAccounts:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.client = TestClient(app)
        self.headers = {"accessKey": "test"}
        self.route = "/accounts"

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
        assert json_response["detail"] == "Missing cif and/or accNum in query parameters."

    @pytest.mark.asyncio
    async def test_customer_does_not_exist(self, mock_mongo):
        """
        Test customer does not exist.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"cif": "11"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Customer does not exist."

    @pytest.mark.asyncio
    async def test_account_does_not_exist(self, mock_mongo):
        """
        Test account does not exist.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "10"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Account does not exist."

    @pytest.mark.asyncio
    async def test_query_by_cif(self, mock_mongo):
        """
        Test query by cif.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0"})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "10"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Account does not exist."

    @pytest.mark.asyncio
    async def test_query_by_accNum(self, mock_mongo):
        """
        Test query by accNum.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "0"})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        response = self.client.get(self.route, headers = self.headers, params = {"accNum": "10"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Account does not exist."

    @pytest.mark.asyncio
    async def test_query_by_cif_accNum(self, mock_mongo):
        """
        Test query by cif and accNum.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0", "accNum": "0"})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0", "accNum": "10"})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["detail"] == "Account does not exist."