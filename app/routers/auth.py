from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth.auth_handler import authenticate_user, create_access_token, get_password_hash, get_user
from ..core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_db
from ..models import User
from ..schemas import Token, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user in the system.

    Parameters:
        user: The user data including username, email, and password
        db: Database session dependency

    Returns:
        UserResponse: The newly created user object

    Raises:
        HTTPException: If the username is already registered
    """
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """Authenticate a user and return an access token.

    Parameters:
        form_data: The OAuth2 password request form containing username and password
        db: Database session dependency

    Returns:
        Token: An object containing the access token and token type

    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
