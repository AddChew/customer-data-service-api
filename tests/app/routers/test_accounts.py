from conftest import date
from app.deployment import app
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