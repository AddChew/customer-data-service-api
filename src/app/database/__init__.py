from datetime import date
from src.app.schemas.customer import Customer


database = [
    Customer(
        cif = "00000001", name = "Bobby Tan", dateOfBirth = date(1995, 10, 2), address = 'address 1', nationality = 'SG', joinDate = date(2000, 1, 1)
    ),
    Customer(
        cif = "00000002", name = "Sally Chan", dateOfBirth = date(1959, 11, 4), address = 'address 2', nationality = 'MY', joinDate = date(2003, 2, 13)
    ),
]