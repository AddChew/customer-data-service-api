from ray import serve
from starlette.requests import Request
from ray.serve._private.http_util import BufferedASGISender


@serve.deployment
class Deployment:
    
    def __init__(self):
        from app import app
        self._app = app

    async def __call__(self, request: Request):
        sender = BufferedASGISender()
        await self._app(request.scope, receive = request.receive, send = sender)
        return sender.build_asgi_response()


deployment = Deployment.bind()