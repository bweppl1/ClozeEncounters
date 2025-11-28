# database schemes pydantic
# validates user input for API requests/responses
from pydantic import BaseModel
from typing import List, Dict


# User model - implement later
# class UserBase(BaseModel):
#     name: str
#
#
# class UserCreate(UserBase):
#     word: Dict[str, List[List[str]]]
#
#
# class UserResponse(UserBase):
#     id: int
#     words: Dict[str, List[List[str]]]
#
#     class Config:
#         orm_mode = True
#
#


# Sentence model
class SentenceBase(BaseModel):
    spanish: str
    english: str


class SentenceCreate(SentenceBase):
    pass


class SentenceResponse(SentenceBase):
    id: int

    class Config:
        from_attributes = True


# Word model
class WordBase(BaseModel):
    word: str


class WordCreate(WordBase):
    word: str
    sentences: List[SentenceBase]


class WordResponse(WordBase):
    id: int
    word: str
    sentences: List[SentenceBase]

    class Config:
        from_attributes = True
