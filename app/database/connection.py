from app.database import settings
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(settings.mongo_uri)
database = client.get_database(settings.customers_database)

customers_collection = database.get_collection(settings.customers_collection)
accounts_collection = database.get_collection(settings.accounts_collection)
transactions_collection = database.get_collection(settings.transactions_collection)