# database schemes pydantic
# validates user input for API requests/responses
from pydantic import BaseModel, ConfigDict
from typing import List, Dict


####################
#  Sentence model  #
####################
class SentenceBase(BaseModel):
    spanish: str
    english: str


class SentenceCreate(SentenceBase):
    pass


class SentenceResponse(SentenceBase):
    pass

    model_config = ConfigDict(from_attributes=True)


####################
#    Word model    #
####################
class WordBase(BaseModel):
    word: str


class WordCreate(WordBase):
    category: List[str]
    sentences: List[SentenceBase]


class WordResponse(WordBase):
    sentences: List[SentenceResponse]

    model_config = ConfigDict(from_attributes=True)

class ClozeResponse(BaseModel):
    word_id: int
    word: str
    answer: str
    cloze: str
    spanish: str
    english: str

###################
#   User model    #
###################
class UserBase(BaseModel):
    email: str
    password: str
    streak: int


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


#######################
#  User Words model   #
#######################
# class UserWordBase(BaseModel):
#     user_id: int
#     word_id: int
#     word_score: List[bool]
#
#
# class UserWordCreate(UserWordBase):
#     pass
#
#
# class UserWordResponse(UserWordBase):
#     user_word_id: int
