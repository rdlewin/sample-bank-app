import pytest

from src.models import Account, User
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.services.user import UserService
from tests.utils import get_random_account_details, get_random_user_details


@pytest.fixture
def user_service(db) -> UserService:
    return UserService(db)


@pytest.fixture
def account_service(db) -> AccountService:
    return AccountService(db)


@pytest.fixture
def transaction_service(db) -> TransactionService:
    return TransactionService(db)


@pytest.fixture
def user(user_service) -> User:
    new_user = user_service.create_user(get_random_user_details())
    yield new_user


@pytest.fixture
def account(account_service, user) -> Account:
    new_account = account_service.create_account(
        get_random_account_details(user.id)
    )
    yield new_account
