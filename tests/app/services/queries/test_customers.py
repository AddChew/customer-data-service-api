import pytest

from app.deployment import setup_app
from fastapi.testclient import TestClient
from conftest import date_string, query_builder


class TestCustomers:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.client = TestClient(setup_app())
        self.headers = {"accessKey": "test"}
        self.route = "/graphql"
        self.query = query_builder(
            query_name = "retrieveCustomer",
            arguments = [{"name": "cif", "value": '"0"'}],
            fields = ["cif", "name", "dateOfBirth", "address", "nationality", "joinDate"],
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
        assert json_response["errors"][0]["path"] == ["retrieveCustomer"]

    def test_invalid_access_key(self):
        """
        Test invalid access key in request headers.
        """
        response = self.client.get(self.route, headers = {"accessKey": "invalid"}, params = {"query": self.query})
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["retrieveCustomer"]

    @pytest.mark.asyncio
    async def test_customer_does_not_exist(self, mock_mongo):
        """
        Test customer does not exist.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveCustomer",
            arguments = [{"name": "cif", "value": '"11"'}],
            fields = ["cif", "name", "dateOfBirth", "address", "nationality", "joinDate"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Customer does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveCustomer"]

    @pytest.mark.asyncio
    async def test_customer_exists(self, mock_mongo):
        """
        Test customer exist.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"query": self.query})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"]["retrieveCustomer"] == {
            "cif": "0",
            "name": "name 0",
            "dateOfBirth": date_string,
            "address": "address 0",
            "nationality": "nationality 0",
            "joinDate": date_string
        }