# data models - SQLAlcehmy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# user model - implement in future
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, index=True)


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

    sentences = relationship("Sentence", back_populates="word")


class Sentence(Base):
    __tablename__ = "sentences"
    id = Column(Integer, primary_key=True)
    spanish = Column(String, nullable=False)
    english = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False, index=True)

    word = relationship("Word", back_populates="sentences")
