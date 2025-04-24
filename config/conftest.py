import pytest
import requests
from faker import Faker
from constant import BASE_URL, AUTH_HEADERS, API_HEADERS

fake = Faker()
@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)

    auth_response = session.post(f"{BASE_URL}/login/access-token", data={"username":"theivangreatgod@mail.ru", "password": "Test12345"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("access_token")
    assert token, "Токен не найден в ответе"

    session.headers.update(API_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})

    return session



@pytest.fixture()
def item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }