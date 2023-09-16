import os

from ray import serve
from fastapi import FastAPI
from app.schemas import Message

from starlette.requests import Request
from ray.serve._private.http_util import BufferedASGISender, RawASGIResponse


def setup_app() -> FastAPI:
    """
    Setup FastAPI application with GraphQL router attached.

    Returns:
        FastAPI: FastAPI application with GraphQL router attached.
    """
    from strawberry import Schema
    from app.services.queries import queries
    from strawberry.tools import create_type
    from strawberry.fastapi import GraphQLRouter

    app = FastAPI(
        title = 'Customer Data Service GraphQL API',
        description = 'Documentation for Customer Data Service GraphQL API',
    )
    schema = Schema(query = create_type(name = 'Query', fields = queries))
    app.include_router(
        router = GraphQLRouter(schema),
        prefix = '/graphql',
        responses = {401: {"model": Message}},
    )
    return app


@serve.deployment(name = 'customer_data_service', num_replicas = int(os.getenv("NUM_REPLICAS", 1)))
class Deployment:
    """
    Customer Data Service API Deployment.
    """
    def __init__(self):
        self.app = setup_app()

    async def __call__(self, request: Request) -> RawASGIResponse:
        """
        Method to handle incoming requests.

        Args:
            request (Request): Incoming request.

        Returns:
            RawASGIResponse: FastAPI application response.
        """
        sender = BufferedASGISender()
        await self.app(request.scope, receive = request.receive, send = sender)
        return sender.build_asgi_response()