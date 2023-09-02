from dotenv import load_dotenv
from app.deployment import Deployment

load_dotenv() # TODO: deprecate once we move to docker
deployment = Deployment.bind()