from typing import List
from fastapi import HTTPException, status

from app.schemas import Customer, Account, Transaction
from app.database.connection import customers_collection, accounts_collection, transactions_collection