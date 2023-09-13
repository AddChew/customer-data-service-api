import pytest

from app.deployment import app
from conftest import date_string
from fastapi.testclient import TestClient


class TestCustomers:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.client = TestClient(app)
        self.headers = {"accessKey": "test"}
        self.route = "/customers"

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
        assert response.status_code == 422
        
        json_response = response.json()
        assert json_response["detail"] == [{'loc': ['query', 'cif'], 'msg': 'field required', 'type': 'value_error.missing'}]

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
    async def test_customer_exists(self, mock_mongo):
        """
        Test customer exist.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"cif": "0"})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response == {
            "cif": "0",
            "name": "name 0",
            "dateOfBirth": date_string,
            "address": "address 0",
            "nationality": "nationality 0",
            "joinDate": date_string
        }