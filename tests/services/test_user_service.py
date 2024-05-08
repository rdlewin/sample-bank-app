import pytest
from sqlalchemy.exc import IntegrityError

import utils
from src.core.utils import hash_password
from tests.utils import get_random_user_details


class TestUserService:
    def test_create_user(self, user_service):
        user_details = get_random_user_details()
        new_user = user_service.create_user(user_details)
        assert new_user.name == user_details.name
        assert new_user.email == user_details.email

    def test_new_user_hashes_password(self, user_service):
        user_details = get_random_user_details()
        new_user = user_service.create_user(user_details)
        assert new_user.hashed_password != user_details.password
        assert new_user.hashed_password == hash_password(user_details.password)

    def test_new_user_duplicate_email_raises_error(self, user_service):
        user_1 = utils.create_user(user_service)
        user_2_details = get_random_user_details()
        user_2_details.email = user_1.email

        with pytest.raises(IntegrityError):
            user_service.create_user(user_2_details)

    def test_get_user_by_id_matches_creation_response(
        self, user_service, user
    ):
        user_service.create_user(utils.get_random_user_details())
        result = user_service.get_user(user.id)
        assert result == user
