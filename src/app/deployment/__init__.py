from ray import serve
from starlette.requests import Request
from ray.serve._private.http_util import BufferedASGISender


def setup_app():
    from fastapi import FastAPI
    from strawberry import Schema
    from src.app.queries import Query
    from strawberry.fastapi import GraphQLRouter

    app = FastAPI(
        title = 'Customer Data Service API',
    )
    schema = Schema(query = Query)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix = '/graphql')

    return app


@serve.deployment(name = 'Customer Data Service', num_replicas = 2)
class Deployment:
    
    def __init__(self):
        self.app = setup_app()

    async def __call__(self, request: Request):
        sender = BufferedASGISender()
        await self.app(request.scope, receive = request.receive, send = sender)
        return sender.build_asgi_response()