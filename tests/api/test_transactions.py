import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder

from src.core.config import settings
from tests import utils


class TestTransactionRoutes:
    def setup_class(self):
        self.root_path = f"{settings.API_V1_PREFIX}/transactions/"

    def test_create_transaction(
        self, db, client, user_service, account_service
    ):
        user_1 = utils.create_user(user_service)
        user_2 = utils.create_user(user_service)

        initial_balance = 100
        account_1 = utils.create_account(
            account_service, user_id=user_1.id, balance=initial_balance
        )
        account_2 = utils.create_account(
            account_service, user_id=user_2.id, balance=initial_balance
        )

        transaction_size = 20
        request = {
            "from_account_id": account_1.id,
            "to_account_id": account_2.id,
            "amount": transaction_size,
            "description": "test",
        }
        response = client.post(self.root_path, json=request)
        assert response.status_code == status.HTTP_201_CREATED

        db.refresh(account_1)
        db.refresh(account_2)
        assert account_1.balance == initial_balance - transaction_size
        assert account_2.balance == initial_balance + transaction_size

    def test_create_transaction_unavailable_funds_raises_error(
        self, db, client, user_service, account_service
    ):
        user_1 = utils.create_user(user_service)
        user_2 = utils.create_user(user_service)

        initial_balance = 100
        account_1 = utils.create_account(
            account_service, user_id=user_1.id, balance=initial_balance
        )
        account_2 = utils.create_account(
            account_service, user_id=user_2.id, balance=initial_balance
        )

        transaction_size = 200
        request = {
            "from_account_id": account_1.id,
            "to_account_id": account_2.id,
            "amount": transaction_size,
            "description": "test",
        }
        response = client.post(self.root_path, json=request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        db.refresh(account_1)
        db.refresh(account_2)
        assert account_1.balance == initial_balance
        assert account_2.balance == initial_balance

    # TODO: Figure out why Pydantic doesn't accept empty lists
    @pytest.mark.xfail()
    def test_get_transactions_no_transactions(
        self, client, user_service, account_service
    ):
        user_1 = utils.create_user(user_service)

        response = client.get(
            f"{settings.API_V1_PREFIX}/users/{user_1.id}/transactions/"
        )
        assert response.status_code == status.HTTP_200_OK
        response_body = jsonable_encoder(response.json())
        assert response_body == []

    def test_get_transactions_returns_users_send_and_receive(
        self, client, user_service, account_service, transaction_service
    ):
        user_1 = utils.create_user(user_service)
        user_2 = utils.create_user(user_service)
        account_1 = utils.create_account(
            account_service, user_id=user_1.id, balance=100
        )
        account_2 = utils.create_account(
            account_service, user_id=user_2.id, balance=100
        )
        transaction_1 = transaction_service.create_transaction(
            utils.get_random_transaction_details(account_1.id, account_2.id)
        )
        transaction_2 = transaction_service.create_transaction(
            utils.get_random_transaction_details(account_2.id, account_1.id)
        )

        response = client.get(
            f"{settings.API_V1_PREFIX}/users/{user_1.id}/transactions/"
        )
        assert response.status_code == status.HTTP_200_OK
        response_body = jsonable_encoder(response.json())
        assert response_body == []
