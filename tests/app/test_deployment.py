from fastapi import FastAPI
from app.deployment import setup_app

# TODO: Update github actions
def test_setup_app(): # TODO: Update pytest
    """
    Test setup_app function.
    """
    app = setup_app()
    assert isinstance(app, FastAPI)
    assert app.title == "Customer Data Service API"

    paths = [route.path for route in app.routes]
    assert "/graphql" in paths