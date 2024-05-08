import pytest
from sqlalchemy.exc import IntegrityError
from utils import get_random_account_details, get_random_user_details


class TestAccountService:
    def test_create_account(self, account_service, user):
        account_details = get_random_account_details(user_id=user.id)
        new_account = account_service.create_account(account_details)
        assert new_account.owner_id == user.id
        assert new_account.transactions_sent == []
        assert new_account.transactions_received == []

    def test_unique_account_names_per_user(self, db, account_service, user):
        new_account = account_service.create_account(
            get_random_account_details(user_id=user.id)
        )

        with pytest.raises(IntegrityError):
            account_service.create_account(
                get_random_account_details(
                    user_id=user.id, name=new_account.name
                )
            )

    def test_unique_names_do_not_block_other_users(
        self, account_service, user_service
    ):
        user_1 = user_service.create_user(get_random_user_details())
        user_2 = user_service.create_user(get_random_user_details())
        account_details = get_random_account_details(user_id=user_1.id)
        account_1 = account_service.create_account(account_details)
        account_details.owner_id = user_2.id
        account_2 = account_service.create_account(account_details)
        assert account_1.owner_id != account_2.owner_id
        assert account_1.name == account_2.name

    def test_get_user_accounts(self, db, account_service, user_service, user):
        other_user = user_service.create_user(get_random_user_details())
        account_service.create_account(
            get_random_account_details(user_id=other_user.id)
        )

        accounts = [
            account_service.create_account(
                get_random_account_details(user_id=user.id)
            )
            for _ in range(3)
        ]

        db.refresh(user)
        assert len(user.accounts) == len(accounts)
        assert sorted(user.accounts, key=lambda account: account.id) == sorted(
            accounts, key=lambda account: account.id
        )

        accounts = account_service.get_accounts(user_id=user.id)
        assert len(user.accounts) == len(accounts)
        assert sorted(user.accounts, key=lambda account: account.id) == sorted(
            accounts, key=lambda account: account.id
        )
