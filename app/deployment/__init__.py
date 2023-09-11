import os

from ray import serve
from fastapi import FastAPI
from app.routers import customers


app = FastAPI(
    title = "Customer Data Service REST API",
    description = "Documentation for Customer Data Service REST API"
)
app.include_router(customers.router)


@serve.deployment(name = 'customer_data_service', num_replicas = int(os.getenv("NUM_REPLICAS", 1)))
@serve.ingress(app)
class Deployment:
    """
    Customer Data Service REST API Deployment.
    """
    pass