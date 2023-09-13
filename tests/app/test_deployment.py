from fastapi import FastAPI
from app.deployment import app


class TestApp:

    def setup_class(self):
        """
        Setup state to be used across tests.
        """
        self.app = app

    def test_isinstance(self):
        """
        Test app isinstance.
        """
        assert isinstance(self.app, FastAPI)

    def test_title(self):
        """
        Test app title.
        """
        assert self.app.title == "Customer Data Service REST API"

    def test_description(self):
        """
        Test app description.
        """
        assert self.app.description == "Documentation for Customer Data Service REST API"

    def test_routes(self):
        """
        Test app routes
        """
        routes = ["/customers", "/accounts", "/transactions"]
        paths = [route.path for route in self.app.routes]
        for route in routes:
            assert route in paths