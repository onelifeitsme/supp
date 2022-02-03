import pytest
from django.contrib.auth.models import User
from tickets.models import Ticket


@pytest.fixture
def new_user_staff(db) -> User:
    """Фикстура создания юзера персонала"""
    return User.objects.create_user(username='staffuser', password='123456', is_staff=True)


@pytest.fixture
def new_user_client(db) -> User:
    """Фикстура создания клиента"""
    return User.objects.create_user(username='clientuser', password='123456', is_staff=False)


@pytest.fixture
def new_ticket(db, new_user_client) -> Ticket:
    """Фикстура создания тикета клиентом"""
    return Ticket.objects.create(type='technical', title='test', description='test_description', user=new_user_client)


@pytest.fixture
def access_jwt_token_client(db, client, new_user_client):
    """Фикстура получения токена клиента"""
    data = {
        "username": new_user_client.username,
        "password": '123456'
    }
    url = 'http://127.0.0.1:8000/auth/jwt/create/'

    response = client.post(url, data=data)
    access_token = response.data['access']
    return access_token


@pytest.fixture
def access_jwt_token_staff(db, client, new_user_staff):
    """Фикстура получения токена персонала"""
    data = {
        "username": new_user_staff.username,
        "password": '123456'
    }
    url = 'http://127.0.0.1:8000/auth/jwt/create/'

    response = client.post(url, data=data)
    access_token = response.data['access']
    return access_token
