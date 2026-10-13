import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_page_returns_200(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assert b"Sign in" in response.content


@pytest.mark.django_db
def test_login_page_renders_username_and_password_fields(client):
    response = client.get(reverse("login"))
    assert b'name="username"' in response.content
    assert b'name="password"' in response.content
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_successful_login_redirects_to_dashboard(client, user):
    response = client.post(
        reverse("login"),
        {"username": user.username, "password": "demo1234"},
    )
    assert response.status_code == 302
    assert response.url == reverse("dashboard")


@pytest.mark.django_db
def test_invalid_password_stays_on_login_with_error(client, user):
    response = client.post(
        reverse("login"),
        {"username": user.username, "password": "wrong-password"},
    )
    assert response.status_code == 200
    assert b"Invalid username or password." in response.content


@pytest.mark.django_db
def test_unknown_user_cannot_log_in(client):
    response = client.post(
        reverse("login"),
        {"username": "missing", "password": "demo1234"},
    )
    assert response.status_code == 200
    assert b"Invalid username or password." in response.content


@pytest.mark.django_db
def test_empty_credentials_show_validation_errors(client):
    response = client.post(reverse("login"), {"username": "", "password": ""})
    assert response.status_code == 200
    assert response.context["form"].errors


@pytest.mark.django_db
def test_dashboard_requires_authentication(client):
    response = client.get(reverse("dashboard"))
    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_logout_ends_session_and_blocks_dashboard(client, user):
    client.force_login(user)
    dashboard = client.get(reverse("dashboard"))
    assert dashboard.status_code == 200
    assert user.username.encode() in dashboard.content

    logout_response = client.get(reverse("logout"))
    assert logout_response.status_code == 302
    assert logout_response.url == reverse("login")

    blocked = client.get(reverse("dashboard"))
    assert blocked.status_code == 302
    assert reverse("login") in blocked.url
