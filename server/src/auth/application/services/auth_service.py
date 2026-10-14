import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from src.shared.config import settings
from src.auth.application.ports.repositories import UserRepositoryInterface
from src.auth.domain.schemas.auth_schemas import UserCreate, Token, UserResponse
from fastapi import HTTPException, status


class AuthService:
    """
    Business logic for Auth
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def _create_access_token(self, data: dict) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user
        """
        # Check if user exists
        existing_user = self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user with hashed password
        hashed_password = self._hash_password(user_data.password)
        user = self.user_repository.create_user(user_data.email, hashed_password)
        return UserResponse.model_validate(user)

    def login_user(self, email: str, password: str) -> Token:
        """
        Login user
        """
        user = self.user_repository.get_user_by_email(email)
        if not user or not self._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self._create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")

    def get_current_user(self, token: str) -> UserResponse:
        """
        Get current authenticated user from JWT token
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            email: str | None = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise credentials_exception

        return UserResponse.model_validate(user)
