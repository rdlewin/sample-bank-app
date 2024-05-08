import random
import uuid
from typing import Optional

from services.account import AccountService
from services.user import UserService
from src import models
from src.schemas import AccountBase, UserCreate


def get_random_name(length=6):
    return uuid.uuid4().hex.lower()[:length]


def get_random_user_details() -> UserCreate:
    return UserCreate(
        email=f"{get_random_name()}@example.com",
        name=get_random_name(),
        password=get_random_name(8),
        balance=100,
    )


def get_random_account_details(
    user_id: int, name: Optional[str] = None, balance: Optional[float] = None
) -> AccountBase:
    if not name:
        name = get_random_name()
    if not balance:
        balance = random.random() * 1000  # Random value 0-1000

    return AccountBase(owner_id=user_id, name=name, balance=balance)


def create_user(user_service: UserService) -> models.User:
    return user_service.create_user(get_random_user_details())


def create_account(
    account_service: AccountService,
    user_id: int,
    name: Optional[str] = None,
    balance: Optional[float] = None,
) -> models.Account:
    return account_service.create_account(
        get_random_account_details(user_id, name, balance)
    )
