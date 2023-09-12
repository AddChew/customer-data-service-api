import os

from ray import serve
from fastapi import FastAPI, Depends
from app.services.authorization import verify_access_key
from app.routers import customers, accounts, transactions


app = FastAPI(
    title = "Customer Data Service REST API",
    description = "Documentation for Customer Data Service REST API",
    dependencies = [Depends(verify_access_key)],
)
app.include_router(customers.router)
app.include_router(accounts.router)


@serve.deployment(name = 'customer_data_service', num_replicas = int(os.getenv("NUM_REPLICAS", 1)))
@serve.ingress(app)
class Deployment:
    """
    Customer Data Service REST API Deployment.
    """
    pass