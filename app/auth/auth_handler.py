from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.config import ALGORITHM, SECRET_KEY
from ..database import get_db
from ..models import User
from ..schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter()

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash.

    Args:
        plain_password: The password in plain text
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash a password for secure storage.

    Args:
        password: The password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """Retrieve a user by username from the database.

    Args:
        db: The database session
        username: The username to search for

    Returns:
        User: The user object if found, None otherwise
    """
    db_user = db.query(User).filter(User.username == username).first()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by verifying their username and password.

    Args:
        db: The database session
        username: The username to authenticate
        password: The password to verify

    Returns:
        User: The authenticated user object if successful, False otherwise
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time delta, defaults to 15 minutes

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Validate an access token and return the current user.

    Args:
        token: The JWT token to validate
        db: The database session

    Returns:
        User: The current user

    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        raise credentials_exception from e

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Return the current active user.

    Args:
        current_user: The current authenticated user

    Returns:
        User: The current authenticated user
    """
    return current_user
