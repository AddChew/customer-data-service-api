import strawberry

from fastapi import FastAPI
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter


access_key = '5803373f2d5bbe604f6454ffd5cc30e3'


@strawberry.type
class Customer:
    cif: str
    name: str


database = [
    Customer(cif = "00000001", name = "Bobby Tan"),
    Customer(cif = "00000002", name = "Sally Chan"),
]


@strawberry.type
class Query:

    @strawberry.field
    def customers(self, cif: Optional[str] = None) -> List[Customer]:
        if cif:
            return list(filter(lambda customer: customer.cif == cif, database))
        return database
    

app = FastAPI()
schema = strawberry.Schema(query = Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix = '/graphql')