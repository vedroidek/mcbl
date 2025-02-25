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

    session = session()
    model = Author

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
        self.check_user = UserIsExists(self.nickname)

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


class UserIsExists:

    def __init__(
            self, 
            user_id: int=None, 
            nickname: str=None
            ):
        self.user_id = user_id
        self.nickname = nickname

    @classmethod
    def get_author_by_id(cls, user_id: int=None):
        if cls.user_id:
            user_id = cls.user_id

        with cls.session.begin() as s:
            user = s.get(cls.model, user_id)
        return user if user else None

    def get_author_by_nickname(self, nickname: str=None):
        if self.nickname:
            nickname = self.nickname
        
        with self.session.begin() as s:
            user = s.execute(select(self.model).where(
                self.model.nickname == nickname
                )).first()
        return user if user else None
    
    def is_exists(self, nickname: str=None, user_id: int=None):
        if self.get_author_by_nickname(nickname) or \
            self.get_author_by_id(user_id):
            return True
        else:
            return False
