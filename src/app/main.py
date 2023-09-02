from dotenv import load_dotenv
from src.app.deployment import Deployment

load_dotenv()
deployment = Deployment.bind()