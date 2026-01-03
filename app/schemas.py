# database schemes pydantic
# validates user input for API requests/responses
from pydantic import BaseModel, ConfigDict, validator
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
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(UserCreate):
    pass

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    user_data: UserResponse
    token: str

##################
#  Token models  #
##################


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


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
