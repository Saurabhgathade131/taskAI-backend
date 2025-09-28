from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        return pwd_ctx.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return pwd_ctx.verify(password, hashed)

    def create_access_token(self, subject: str) -> str:
        exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": subject, "exp": exp}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
