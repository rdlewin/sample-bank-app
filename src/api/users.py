from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas import Account, AccountBase, Transaction, User, UserCreate
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.services.user import UserService

router = APIRouter()


@router.get("/")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserService(db).get_users(skip, limit)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    result = UserService(db).get_user(user_id)
    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User {user_id} not found"
        )
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    new_user = UserService(db).create_user(user)
    AccountService(db).create_account(
        AccountBase(owner_id=new_user.id, name="Default", balance=user.balance)
    )
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}/accounts")
def list_accounts(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[Account]:
    return AccountService(db).get_accounts(user_id, skip, limit)


@router.get("/{user_id}/transactions")
def list_transactions(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[Transaction]:
    return TransactionService(db).get_transactions(user_id, skip, limit)
