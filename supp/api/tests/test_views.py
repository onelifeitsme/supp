from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from tickets.models import Ticket


def test_authorization_without_token(db, client):
    """Тест авторизации без токена"""
    url = reverse('tickets')
    response = client.get(path=url)
    assert response.status_code == 401


def test_authorization_with_token(db, client, access_jwt_token_client):
    """Тест авторизации c полученным токеном"""
    url = reverse('tickets')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_client)
    response = client.get(path=url)
    assert response.status_code == 200


def test_create_new_ticket(db, client, access_jwt_token_client):
    """Тест создания нового тикета клиентом"""
    url = reverse('tickets')
    data = {
        "type": "Технические вопросы",
        "title": "тестовый тикет",
        "description": "описание тестового тикета тикета"
    }

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_client)
    response = client.post(path=url, data=data)
    assert 'Новый тикет успешно создан' in response.data


def test_aliens_tickets_visibility(db, client, new_user_staff, new_user_client, access_jwt_token_client):
    """Тест видимости чужих тикетов клиенту"""
    Ticket.objects.create(type="Технические вопросы",
                          title="чужой тикет",
                          description="описание",
                          user=new_user_staff
                          )
    Ticket.objects.create(type="Технические вопросы",
                          title="свой тикет",
                          description="описание",
                          user=new_user_client
                          )
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_client)
    url = reverse('tickets')
    response = client.get(path=url)
    assert 'чужой тикет' not in str(response.data)


def test_change_ticket_status(db, client, new_ticket, access_jwt_token_staff):
    """Тест обновления статуса тикета"""
    url = new_ticket.get_absolute_url()
    data = {"status": "Принят в работу"}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_staff)
    client.patch(path=url, data=data)
    ticket = Ticket.objects.get(pk=new_ticket.pk)
    assert ticket.status == 'Принят в работу'


def test_write_ticket_message(db, client, new_ticket, access_jwt_token_client):
    """Тест написания сообщения в тикете"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_client)
    url = f'{new_ticket.get_absolute_url()}/messages'
    data = {"text": "some text"}

    response = client.post(path=url, data=data)
    assert 'Сообщение отправлено' in response.data


def test_is_spamer(client, new_ticket, access_jwt_token_client):
    """Тест проверяет, не пытается ли клиент написать больше 3 сообщений подряд"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_jwt_token_client)
    url = f'{new_ticket.get_absolute_url()}/messages'
    data = {"text": "some text"}
    for i in range(4):
        response = client.post(path=url, data=data)
    assert 'Дождитесь ответа от администрации' in response.data
