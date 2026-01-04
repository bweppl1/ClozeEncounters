from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth.auth_handler import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)
from ..core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_db
from ..models import User
from ..schemas import LoginResponse, UserCreate, UserLogin, Token

router = APIRouter()


@router.post("/register", response_model=LoginResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user in the system.

    Parameters:
        user: The user data including email, email, and password
        db: Database session dependency

    Returns:
        UserResponse: The newly created user object

    Raises:
        HTTPException: If the email is already registered
    """
    db_user = get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"DEBUG user id: {db_user.id}")

    # create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return({"user_data":db_user, "token":access_token})

@router.post("/login", response_model=LoginResponse)
async def login(user: UserLogin, db: Session = Depends(get_db))
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return({"user_data":user, "token":access_token})
