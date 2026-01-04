from fastapi import APIRouter, Depends

from ..auth.auth_handler import get_current_user
from ..models import User
from ..schemas import UserResponse

router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # arg is the storedToken from localStorage, handled by get_current_user
    return current_user
