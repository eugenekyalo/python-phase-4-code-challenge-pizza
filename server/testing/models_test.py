from app import app, db
from models import Restaurant, Pizza, RestaurantPizza
from faker import Faker
import pytest

def test_price_between_1_and_30():
    '''requires price between 1 and 30.'''

    with app.app_context():

        pizza = Pizza(
            name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address='Main St')
        db.session.add(pizza)
        db.session.add(restaurant)
        db.session.commit()

        # Test with valid price
        restaurant_pizza = RestaurantPizza(
            price=20, pizza_id=pizza.id, restaurant_id=restaurant.id)
        db.session.add(restaurant_pizza)
        db.session.commit()
        assert restaurant_pizza.price == 20

        # Test with invalid price
        try:
            restaurant_pizza_invalid = RestaurantPizza(
                price=50, pizza_id=pizza.id, restaurant_id=restaurant.id)
            db.session.add(restaurant_pizza_invalid)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            assert str(e) == "Price must be between 1 and 30"
