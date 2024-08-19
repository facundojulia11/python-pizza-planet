from faker import Faker
from random import choice, randint, sample
from app.plugins import db, ma
from app import flask_app
from app.scripts.utils import fake_data
from app.repositories.models import Order, OrderDetail, Ingredient, Size, Beverage
from app.services.services import create, update, get_all, get_by_id

fake = Faker()

ingredients_seeder = fake_data.ingredient_seeder
users_seeder = fake_data.user_seeder
sizes_seeder = fake_data.size_seeder
beverages_seeder = fake_data.beverage_seeder

def fake_price() -> int:
    return fake.random_int(min=2, max=10)

def create_ingredients():
    with flask_app.app_context():
        for index in range(10):
            db.session.add(Ingredient(
                name=ingredients_seeder[index],
                price=fake_price()
            ))
        db.session.commit()

def create_beverages():
    with flask_app.app_context():
        for index in range(10):
            db.session.add(Beverage(
                name=beverages_seeder[index],
                price=fake_price()
            ))
        db.session.commit()

def create_sizes():
    with flask_app.app_context():
        for index in range(5):
            db.session.add(Size(
                name=sizes_seeder[index],
                price=index+10
            ))
        db.session.commit()

def create_orders():
    with flask_app.app_context():
        for _ in range(100):
            client = choice(users_seeder)
            size = choice(db.session.query(Size).all())
            order = Order(
                client_name=client["client_name"],
                client_dni=client["client_dni"],
                client_address=client["client_address"],
                client_phone=client["client_phone"],
                date=fake.date_time_between(start_date='-12M', end_date='now'),
                size_id=size._id,
                total_price=size.price,  # Start with the size price
            )

            db.session.add(order)
            db.session.commit()

            random_beverages = get_unique_random_items(db.session.query(Beverage).all(), randint(1,5))
            random_ingredients = get_unique_random_items(db.session.query(Ingredient).all(), randint(1,5))

            total_price = size.price
            for ingredient in random_ingredients:
                order_detail = OrderDetail(
                    order_id=order._id,
                    ingredient_id=ingredient._id,
                )
                db.session.add(order_detail)
                total_price += ingredient.price

            for beverage in random_beverages:
                order_detail = OrderDetail(
                    order_id=order._id,
                    beverage_id=beverage._id,
                )
                db.session.add(order_detail)
                total_price += beverage.price

            order.total_price = total_price
            db.session.commit()

def get_unique_random_numbers(max_value, count):
    if count > max_value:
        raise ValueError("Count cannot be greater than the maximum value")
    return sample(range(1, max_value+1), count)

def get_unique_random_items(items, count):
    if count > len(items):
        raise ValueError("Count cannot be greater than the number of items available")
    selected_indices = get_unique_random_numbers(len(items), count)
    return [items[i - 1] for i in selected_indices]

def remove_product(Model):
    with flask_app.app_context():
        try:
            db.session.query(Model).delete()
            db.session.commit()
            return f"All {Model.__name__} records have been removed successfully."
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
        
from sqlalchemy import func
from app.repositories.models import OrderDetail, Ingredient

def remove_all():
    remove_product(Size)
    remove_product(Ingredient)
    remove_product(Beverage)
    remove_product(Order)
    remove_product(OrderDetail)

def main():
    remove_all()
    create_ingredients()
    create_sizes()
    create_beverages()
    create_orders()

if __name__ == "__main__":
    main()
