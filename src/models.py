import datetime
from enum import Enum

from sqlalchemy import Double, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class TransactionStatus(Enum):
    DONE = "DONE"
    CANCELED = "CANCELED"
    REFUNDED = "REFUNDED"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    last_updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    accounts: Mapped[list["Account"]] = relationship(back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    owner_id = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    balance: Mapped[float] = mapped_column(Double, nullable=False, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    last_updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    owner: Mapped["User"] = relationship(back_populates="accounts")
    transactions_sent: Mapped[list["Transaction"]] = relationship(
        foreign_keys="Transaction.from_account_id",
        lazy=True,
        order_by="Transaction.created_at",
    )
    transactions_received: Mapped[list["Transaction"]] = relationship(
        foreign_keys="Transaction.to_account_id",
        lazy=True,
        order_by="Transaction.created_at",
    )

    __table_args__ = (
        Index("idx_accounts_unique_owner_name", owner_id, name, unique=True),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False
    )
    to_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(Double, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        nullable=False, default=TransactionStatus.DONE
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    from_account: Mapped["Account"] = relationship(
        "Account",
        back_populates="transactions_sent",
        foreign_keys="Transaction.from_account_id",
    )
    to_account: Mapped["Account"] = relationship(
        "Account",
        back_populates="transactions_received",
        foreign_keys="Transaction.to_account_id",
    )
