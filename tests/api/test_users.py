from fastapi import status

from src import schemas
from src.core.config import settings
from tests.utils import get_random_user_details


class TestUserRoutes:
    def setup_class(self):
        self.root_path = f"{settings.API_V1_PREFIX}/users/"

    def test_create_user(self, client, user_service):
        user_details = get_random_user_details()
        response = client.post(self.root_path, json=user_details.dict())
        assert response.status_code == status.HTTP_201_CREATED

        response_body = dict(response.json())
        new_user_id = int(response_body["id"])
        response_body.pop("accounts")  # Testing that separately
        assert response_body == {
            "email": user_details.email,
            "id": new_user_id,
            "is_active": True,
            "name": user_details.name,
        }

    def test_new_user_created_with_default_account(self, client, user_service):
        user_details = get_random_user_details()
        response = client.post(self.root_path, json=user_details.dict())
        assert response.status_code == status.HTTP_201_CREATED

        response_body = dict(response.json())
        assert len(response_body["accounts"]) == 1
        assert response_body["accounts"][0]["owner_id"] == response_body["id"]
        assert response_body["accounts"][0]["balance"] == user_details.balance

    def test_get_user(self, client, user):
        response = client.get(f"{self.root_path}{user.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == schemas.User.from_orm(user).dict()
