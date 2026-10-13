import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username="demo",
        email="demo@example.com",
        password="demo1234",
    )


@pytest.fixture
def client():
    from django.test import Client

    return Client()
