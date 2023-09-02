from dotenv import load_dotenv
from src.app.deployment import Deployment


print(load_dotenv(dotenv_path = "./../.env")) # TODO: fix dotenv issue
deployment = Deployment.bind()