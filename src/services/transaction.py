from sqlalchemy import text
from sqlalchemy.exc import InternalError
from sqlalchemy.orm import Session

from src import schemas
from src.models import Transaction
from src.services.base import BaseService


class TransactionService(BaseService):
    def __init__(self, db: Session):
        super().__init__(Transaction, db)

    def get_transaction(self, account_id: int) -> Transaction:
        return self._get(account_id)

    def get_transactions(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Transaction]:
        return self._get_list(
            {
                "OR": {
                    "from_account.owner_id": user_id,
                    "to_account.owner.id": user_id,
                }
            },
            skip,
            limit,
        )

    def create_transaction(
        self, transaction: schemas.TransactionBase
    ) -> Transaction:
        """
        Transfer funds from one account to another
        This is done in two separate queries, but a single transaction:
        The first part, transferring funds, is done as a single query on the DB to avoid race conditions
        The second part, creating the transaction log, is only done if the first part passes,
        since it is on a separate table, it can safely run as a separate request, minimising the time that accounts is locked
        """
        params = {
            "from_account_id": transaction.from_account_id,
            "to_account_id": transaction.to_account_id,
            "amount": transaction.amount,
        }
        try:
            self.db.execute(
                text(
                    """
                DO
                $$
                    BEGIN
                        IF ((SELECT balance FROM accounts WHERE id = :from_account_id) - :amount) < 0 THEN
                            RAISE EXCEPTION 'Insufficient funds in sender''s account';
                        END IF;
                
                        UPDATE accounts
                        SET balance = balance - :amount
                        WHERE id = :from_account_id;
                
                        UPDATE accounts
                        SET balance = balance + :amount
                        WHERE id = :to_account_id;
                    END;
                $$
                """
                ),
                params=params,
            )
        except InternalError:
            raise ValueError(
                f"Account {transaction.from_account_id} does not have enough funds to send {transaction.amount}"
            )

        new_transaction = Transaction(
            from_account_id=transaction.from_account_id,
            to_account_id=transaction.to_account_id,
            amount=transaction.amount,
            description=transaction.description,
        )
        return self._create_instance(new_transaction)

    def delete_transaction(self, transaction_id: int):
        self._delete_instance(transaction_id)
