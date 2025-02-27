from sqlalchemy import exc, select, or_
from pydantic import BaseModel, EmailStr, Field
from . models import Author
from .database import session


class UserData(BaseModel):
    
    nickname: str = Field(
        min_length=3, max_length=64, kw_only=True
        )
    email_address: EmailStr = Field(
        strict=True, 
        pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        kw_only=True
        )
    password: str = Field(
        strict=True, min_length=6, max_length=128, kw_only=True
        )


class AuthorRepo:
    """It accepts the data transferred by the user and, 
    if they are correctly, retains in the database.
    
    Keyword arguments:
    nickname -- str 
    email_address -- str (The email address is compared
      with a regular expression template)
    password -- str (len between 6 and 128 chars)
    """
    model = Author
    session = session()

    def __init__(self, nickname, email_address, password):
        self.user = UserData(
            nickname = nickname, 
            email_address = email_address, 
            password = password
            )

    @classmethod
    def get_all_users(cls):
        with cls.session.begin() as s:
            s.execute()

    @classmethod
    def get_author_by_id(cls, user_id: int):
        with cls.session.begin() as s:
            user = s.get(cls.model, user_id).as_dict()
        return user if user else None

    def is_exists(self, nickname: str, email_address: str):
        with self.session.begin() as s:
            user = s.execute(
                select(self.model).filter(
                    or_(self.model.nickname == nickname, 
                        self.model.email_address == email_address))
                        ).first()
            
        return user if user else None

    def save(self) -> str:
        with self.session.begin() as s:
            try:
                s.add(self.model(**self.user.model_dump()))
                s.commit()
                return "The data is saved successfully."
            except exc.DatabaseError as e:
                s.rollback()
                return e._message()
