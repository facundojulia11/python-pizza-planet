import random
from faker import Faker

fake = Faker()

def create_fake_users(num_of_users=10):
    users = []
    for _ in range(num_of_users):
        users.append({
            "client_name": fake.name(),
            "client_dni": random.randint(1000000000, 9999999999),
            "client_address": fake.address(),
            "client_phone": random.randint(1000000000, 9999999999)
        })
    return users


size_seeder = [
    "Small", 
    "Medium", 
    "XL", 
    "XXL", 
    "Colossal"
]

ingredient_seeder = [
    "Salami", 
    "Cheddar", 
    "Green Olives", 
    "Bell Peppers", 
    "Chicken",
    "Sausage", 
    "Gorgonzola", 
    "Caramelized Onions", 
    "Spinach", 
    "Pineapple"
]

beverage_seeder = [
    "Mountain Dew", 
    "Dr Pepper", 
    "Fanta", 
    "Ginger Ale",
    "Root Beer",
    "Tropicana",
    "Snapple", 
    "Peach Iced Tea", 
    "Lemonade", 
    "Mineral Water"
]

user_seeder = create_fake_users()



