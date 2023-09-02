from dotenv import load_dotenv
from src.app.deployment import Deployment

load_dotenv() # TODO: deprecate once we move to docker
deployment = Deployment.bind()