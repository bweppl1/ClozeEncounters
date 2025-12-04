# data models - SQLAlcehmy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

    sentences = relationship("Sentence", back_populates="word")
    word_score = relationship("UserWords", back_populates="word")


class Sentence(Base):
    __tablename__ = "sentences"
    id = Column(Integer, primary_key=True)
    spanish = Column(String, nullable=False)
    english = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    word = relationship("Word", back_populates="sentences")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, default="password")
    streak = Column(Integer, default=0)
    experience = Column(Integer, default=0)
    level = Column(Integer, default=0)


class UserWords(Base):
    __tablename__ = "user_words"
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_score = Column(ARRAY[Boolean])

    word = relationship("Word", back_populates="word_score")
