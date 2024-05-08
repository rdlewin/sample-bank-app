from typing import Optional

from pydantic import BaseModel

from src.models import TransactionStatus


class AccountBase(BaseModel):
    owner_id: int
    name: str
    balance: float


class Account(AccountBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str
    balance: float

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    is_active: bool
    accounts: list[Account] = []

    class Config:
        from_attributes = True
        orm_mode = True


class TransactionBase(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    description: Optional[str]


class Transaction(TransactionBase):
    from_owner_id: int
    from_account_name: str
    to_owner_id: int
    to_account_name: str
    status: TransactionStatus

    @classmethod
    def from_orm(cls, obj) -> "Transaction":
        return cls(
            from_account_id=obj.from_account_id,
            to_account_id=obj.to_account_id,
            amount=obj.amount,
            description=obj.description,
            to_owner_id=obj.to_account.owner_id,
            from_owner_id=obj.from_account.owner_id,
            to_account_name=obj.to_account.name,
            from_account_name=obj.from_account.name,
            status=obj.status,
        )
