from app.database import SessionLocal
from app.models import Word, User, UserWords

db = SessionLocal()

def get_user(user):
    user_found = db.query(User).filter(User.name == user).first()

    if user_found:
        return user_found
    else:
        user = User(name=user)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
