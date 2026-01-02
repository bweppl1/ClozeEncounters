from fastapi import APIRouter, Depends

from ..auth.auth_handler import get_current_active_user
from ..models import User
from ..schemas import UserResponse

router = APIRouter()


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information.

    Args:
        current_user (User): The authenticated user retrieved from the token.
            This is handled by the get_current_active_user dependency.

    Returns:
        UserResponse: A JSON representation of the current user.
    """
    return current_user
