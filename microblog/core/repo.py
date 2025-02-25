from sqlalchemy import exc, select
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

    Session = session()
    Model = Author

    def __init__(self, nickname, email_address, password, id: int=None):
        self.id = id
        self.nickname = nickname
        self.email_address = email_address
        self.password = password
        self.user = UserData(
            nickname = nickname, 
            email_address = email_address, 
            password = password
            )

    def save(self) -> bool:
        with self.Session.begin() as s:
            try:
                s.add(self.Model(**self.user.model_dump()))
                s.commit()
                return True
            except exc.DatabaseError as e:
                s.rollback()
                e._message()
                return False

    def get_author_by_id(self, id):
        with self.Session.begin() as s:
            if author_id := (s.get(self.Model, id).id):
                return author_id
            else:
                return None
            
    def is_exists(self, nickname: str):
        if self.get_author_by_nickname(nickname):
            return True
        else:
            return False

           
    def get_author_by_nickname(self, nickname):
        with self.Session.begin() as s:
            if author := (s.execute(select(self.Model).where(
                self.Model.nickname == nickname)).first()):
                return author
            else:
                return None
