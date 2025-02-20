import hashlib
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
        strict=True, min_length=6, max_length=128, kw_only=True,
        default_factory=lambda: hashlib.sha3_256()
        )


class AuthorRepo:
    def __init__(self, nickname, email_address, password, id: int=None):
        self.id = id
        self.user = UserData(
            nickname = nickname, 
            email_address = email_address, 
            password = password
            )
        self.model = Author
        self.session = session()

    def save(self) -> bool:
        with self.session.begin() as s:
            try:
                s.add(self.model(**self.user.model_dump()))
                s.commit()
                return True
            except exc.DatabaseError as e:
                s.rollback()
                e._message()
                return False

    def get_author_by_id(self, id):
        with self.session.begin() as s:
            if author_id := (s.get(self.model, id).id):
                return author_id
            else:
                return None
            
    def get_author_by_nickname(self, nickname):
        with self.session.begin() as s:
            stmt = select(self.model).where(self.model.nickname == nickname)
            author = s.execute(stmt).fetchone()
            return author.as_scalar()
