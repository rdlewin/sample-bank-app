import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas import Account, AccountBase
from src.services.account import AccountService

router = APIRouter()


@router.get("/{account_id}", status_code=status.HTTP_200_OK)
def get_account(account_id: int, db: Session = Depends(get_db)) -> Account:
    return AccountService(db).get_account(account_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountBase, db: Session = Depends(get_db)
) -> Account:
    try:
        return AccountService(db).create_account(account)
    except ValueError as e:
        logging.error(e)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"error": str(e)}
        )
