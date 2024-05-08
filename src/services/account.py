from sqlalchemy.orm import Session

from src import schemas
from src.models import Account
from src.services.base import BaseService


class AccountService(BaseService):
    def __init__(self, db: Session):
        super().__init__(Account, db)

    def get_account(self, account_id: int) -> Account:
        return self._get(account_id)

    def get_accounts(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Account]:
        return self._get_list({"owner_id": user_id}, skip, limit)

    def create_account(self, account: schemas.AccountBase) -> Account:
        new_account = Account(
            owner_id=account.owner_id,
            name=account.name,
            balance=account.balance,
        )
        return self._create_instance(new_account)

    def delete_account(self, account_id: int):
        self._delete_instance(account_id)
