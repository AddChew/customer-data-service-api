import os
from faker import Faker


seed = int(os.getenv('FIXTURES_SEED', 0))
num_customers = int(os.getenv('NUM_CUSTOMERS', 100))

Faker.seed(seed)
fake = Faker()


def generate_customers_fixture():
    customers = []
    for _ in range(num_customers):
        dateOfBirth = fake.date_of_birth(minimum_age = 21, maximum_age = 80)
        joinDate = fake.past_date(dateOfBirth)

        customer = dict(
            cif = fake.unique.bban(),
            name = fake.unique.name(),
            dateOfBirth = dateOfBirth,
            address = fake.unique.address(),
            nationality = fake.country_code(),
            joinDate = joinDate,
        )
        customers.append(customer)
    return customers