import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas import Transaction, TransactionBase
from src.services.transaction import TransactionService

router = APIRouter()


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int, db: Session = Depends(get_db)
) -> Transaction:
    return TransactionService(db).get_transaction(transaction_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def transfer_funds(
    transaction: TransactionBase, db: Session = Depends(get_db)
) -> Transaction:
    try:
        result = TransactionService(db).create_transaction(transaction)
    except ValueError as e:
        logging.warning(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="foo"
        )
    return Transaction.from_orm(result)
