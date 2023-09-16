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
            query_name = "retrieveAccounts",
            arguments = [{"name": "cif", "value": '"0"'}, {"name": "accNum", "value": '"0"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
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
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    def test_invalid_access_key(self):
        """
        Test invalid access key in request headers.
        """
        response = self.client.get(self.route, headers = {"accessKey": "invalid"}, params = {"query": self.query})
        assert response.status_code == 401
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing or invalid access key in request headers"
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    def test_missing_query_params(self):
        """
        Test missing query parameters.
        """
        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 400
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Missing cif and/or accNum in query parameters."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    @pytest.mark.asyncio
    async def test_customer_does_not_exist(self, mock_mongo):
        """
        Test customer does not exist.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "cif", "value": '"11"'}, {"name": "accNum", "value": '"0"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Customer does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    @pytest.mark.asyncio
    async def test_account_does_not_exist(self, mock_mongo):
        """
        Test account does not exist.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "accNum", "value": '"10"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404

        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    @pytest.mark.asyncio
    async def test_query_by_cif(self, mock_mongo):
        """
        Test query by cif.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "cif", "value": '"0"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"]["retrieveAccounts"] == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "cif", "value": '"10"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    @pytest.mark.asyncio
    async def test_query_by_accNum(self, mock_mongo):
        """
        Test query by accNum.
        """
        await mock_mongo
        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "accNum", "value": '"0"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"]["retrieveAccounts"] == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "accNum", "value": '"10"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]

    @pytest.mark.asyncio
    async def test_query_by_cif_accNum(self, mock_mongo):
        """
        Test query by cif and accNum.
        """
        await mock_mongo
        response = self.client.get(self.route, headers = self.headers, params = {"query": self.query})
        assert response.status_code == 200
        
        json_response = response.json()
        assert json_response["data"]["retrieveAccounts"] == [{
            "accHolderCif": "0",
            "accHolderName": "name 0",
            "accNum": "0",
            "accStatus": "accStatus 0",
            "accType": "accType 0",
            "createDate": date_string,
            "currency": "currency 0"
        }]

        query = query_builder(
            query_name = "retrieveAccounts",
            arguments = [{"name": "cif", "value": '"0"'}, {"name": "accNum", "value": '"10"'}],
            fields = ["accHolderCif", "accHolderName", "accNum", "accStatus", "accType", "createDate", "currency"],
        )
        response = self.client.get(self.route, headers = self.headers, params = {"query": query})
        assert response.status_code == 404
        
        json_response = response.json()
        assert json_response["data"] is None
        assert json_response["errors"][0]["message"] == "Account does not exist."
        assert json_response["errors"][0]["path"] == ["retrieveAccounts"]