import pytest

from main import app
from auth_dependencies import get_current_user
from models.user import User
from enums.user_role import UserRole


@pytest.fixture
def admin_user():
    return User(
        id=1,
        username="admin_test",
        hashed_password="dummy_hash",
        role=UserRole.ADMIN,
        is_active=True
    )


@pytest.fixture
def authenticated_client(admin_user):
    from fastapi.testclient import TestClient

    app.dependency_overrides[get_current_user] = (
        lambda: admin_user
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()