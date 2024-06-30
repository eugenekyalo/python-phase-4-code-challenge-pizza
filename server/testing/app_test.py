from app import app, db
from models import Restaurant, Pizza, RestaurantPizza
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()


def test_get_restaurants(client):
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_restaurant(client):
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    db.session.add(restaurant)
    db.session.commit()

    response = client.get(f'/restaurants/{restaurant.id}')
    assert response.status_code == 200
    assert response.json['name'] == "Test Restaurant"

def test_delete_restaurant(client):
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    db.session.add(restaurant)
    db.session.commit()

    response = client.delete(f'/restaurants/{restaurant.id}')
    assert response.status_code == 204

    response = client.get(f'/restaurants/{restaurant.id}')
    assert response.status_code == 404

def test_get_pizzas(client):
    response = client.get('/pizzas')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_restaurant_pizza(client):
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    pizza = Pizza(name="Test Pizza", ingredients="Dough, Cheese, Tomato Sauce")
    db.session.add(restaurant)
    db.session.add(pizza)
    db.session.commit()

    response = client.post('/restaurant_pizzas', json={
        "price": 10,
        "pizza_id": pizza.id,
        "restaurant_id": restaurant.id
    })

    assert response.status_code == 201
    assert response.json['price'] == 10
    assert response.json['pizza']['name'] == "Test Pizza"
    assert response.json['restaurant_id'] == restaurant.id

def test_create_restaurant_pizza_validation_error(client):
    # Invalid price (out of range)
    response = client.post('/restaurant_pizzas', json={
        "price": 50,
        "pizza_id": 1,
        "restaurant_id": 1
    })
    assert response.status_code == 400

    # Invalid pizza_id (non-existent)
    response = client.post('/restaurant_pizzas', json={
        "price": 10,
        "pizza_id": 9999,
        "restaurant_id": 1
    })
    assert response.status_code == 400

    # Invalid restaurant_id (non-existent)
    response = client.post('/restaurant_pizzas', json={
        "price": 10,
        "pizza_id": 1,
        "restaurant_id": 9999
    })
    assert response.status_code == 400
