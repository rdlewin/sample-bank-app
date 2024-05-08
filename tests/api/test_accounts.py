from fastapi import status
from fastapi.encoders import jsonable_encoder

import utils
from core.config import settings
from schemas import AccountBase


class TestAccountRoutes:
    def setup_class(self):
        self.root_path = f"{settings.API_V1_PREFIX}/accounts/"

    def test_create_account(self, client, user):
        request = AccountBase(owner_id=user.id, name="test", balance=100)
        response = client.post(self.root_path, json=request.dict())
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_create_account_unique_account_names_per_user(self, client, user):
        request = AccountBase(owner_id=user.id, name="test", balance=100)
        response = client.post(self.root_path, json=request.dict())
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post(self.root_path, json=request.dict())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_accounts_returns_only_user(
        self, client, user_service, account_service
    ):
        user_1 = utils.create_user(user_service)
        user_2 = utils.create_user(user_service)
        account_1 = utils.create_account(account_service, user_id=user_1.id)
        account_2 = utils.create_account(account_service, user_id=user_1.id)
        account_3 = utils.create_account(account_service, user_id=user_1.id)
        utils.create_account(account_service, user_id=user_2.id)

        response = client.get(
            f"{settings.API_V1_PREFIX}/users/{user_1.id}/accounts/"
        )
        assert response.status_code == status.HTTP_200_OK
        response_body = jsonable_encoder(response.json())
        reponse_account_ids = [account["id"] for account in response_body]
        assert reponse_account_ids == [
            account_1.id,
            account_2.id,
            account_3.id,
        ]
