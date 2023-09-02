from dotenv import load_dotenv
from src.app.deployment import Deployment


load_dotenv(dotenv_path = ".../.env")
deployment = Deployment.bind()