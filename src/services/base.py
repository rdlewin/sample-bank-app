from typing import Optional

from sqlalchemy.orm import Session

from src.core.db import Base


class BaseService:
    def __init__(self, db_type: type[Base], db: Session):
        self.db = db
        self.db_type = db_type

    def _get(self, instance_id: int):
        return (
            self.db.query(self.db_type)
            .filter(self.db_type.id == instance_id)
            .first()
        )

    def _get_list(
        self, filters: Optional[dict] = None, skip: int = 0, limit: int = 100
    ):
        query = self.db.query(self.db_type)
        if filters:
            query = query.filter_by(**filters)

        return query.order_by("id").offset(skip).limit(limit).all()

    def _create_instance(self, instance: Base):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def _delete_instance(self, instance_id: int):
        instance = self._get(instance_id)
        self.db.delete(instance)
