import pytest
import requests
from faker import Faker
from constant import BASE_URL, HEADERS

fake = Faker()
@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/login/access-token", data={"username":"theivangreatgod@mail.ru", "password": "Test12345"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("access_token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"authorization": f"access_token={token}"})

    return session



@pytest.fixture()
def booking_data():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }