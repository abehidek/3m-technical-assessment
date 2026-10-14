from fastapi import APIRouter, Depends, Response, Cookie, status
from sqlalchemy.orm import Session
from typing import Optional

from src.shared.database import get_db
from src.auth.domain.schemas.auth_schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from src.auth.infrastructure.repositories.user_repository import UserRepository
from src.auth.application.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """
    Creates AuthService with deps
    """
    user_repository = UserRepository(db)
    return AuthService(user_repository)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    """
    return auth_service.register_user(user_data)


@router.post("/login")
def login(
    user_data: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Login user and set httpOnly cookie w/ JWT
    """
    token = auth_service.login_user(user_data.email, user_data.password)

    # Set httpOnly cookie for security
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,  # JavaScript cannot access
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=1800,  # 30 minutes
    )

    return {
        "message": "Login successful",
        "access_token": token.access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response):
    """
    Logout user by removing the cookie
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
def get_current_user(
    access_token: Optional[str] = Cookie(None),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Get current authenticated user from httpOnly cookie
    """
    if not access_token:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return auth_service.get_current_user(access_token)
