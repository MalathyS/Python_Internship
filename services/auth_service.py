
from fastapi import HTTPException, status

from models.user import UserRole
from repositories.user_repository import UserRepository
from schemas.user import UserCreate
from utilities.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, user_data: UserCreate):
        # 1. Check whether username already exists
        existing_user = (
            await self.user_repository.get_by_username(
                user_data.username
            )
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        # 2. Hash the password before saving it
        hashed_password = hash_password(user_data.password)

        # 3. Create the user with the default Employee role
        user = await self.user_repository.create(
            username=user_data.username,
            password_hash=hashed_password,
            role=UserRole.EMPLOYEE,
        )

        return user

    async def login(self, username: str, password: str):
        # 1. Find the user
        user = await self.user_repository.get_by_username(username)

        # 2. Verify credentials
        if not user or not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Reject inactive accounts
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # 4. Generate JWT using your existing security utility
        token = create_access_token(
            subject=str(user.id),
            role=user.role,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
