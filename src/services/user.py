from sqlalchemy.orm import Session

from src import schemas
from src.core import utils
from src.models import User
from src.services.base import BaseService


class UserService(BaseService):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_user(self, user_id: int) -> User:
        return self._get(user_id)

    def get_users(self, skip: int = 0, limit: int = 100):
        return self._get_list(None, skip, limit)

    def create_user(self, user: schemas.UserCreate):
        password_hashed = utils.hash_password(user.password)
        new_user = User(
            email=user.email, name=user.name, hashed_password=password_hashed
        )
        self._create_instance(new_user)
        return new_user

    def delete_user(self, user_id: int):
        self._delete_instance(user_id)
