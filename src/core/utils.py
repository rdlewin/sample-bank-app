import base64
import hashlib
import hmac

from src.core.config import settings


def hash_password(password: str) -> str:
    digest = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        msg=password.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(digest).decode()
