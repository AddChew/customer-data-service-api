from fastapi import FastAPI
from app.deployment import setup_app


def test_setup_app():
    """
    Test setup_app function.
    """
    app = setup_app()
    assert isinstance(app, FastAPI)
    assert app.title == "Customer Data Service API"

    paths = [route.path for route in app.routes]
    assert "/graphql" in paths