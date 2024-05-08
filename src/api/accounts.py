from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas import Account, AccountBase
from src.services.account import AccountService

router = APIRouter()


@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)) -> Account:
    return AccountService(db).get_account(account_id)


@router.post("/")
def create_account(
    account: AccountBase, db: Session = Depends(get_db)
) -> Account:
    return AccountService(db).create_account(account)
