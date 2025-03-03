import hashlib
import os
from sqlalchemy import exc, select, or_, update
from pydantic import BaseModel, EmailStr, Field
from . models import Author
from .database import session


def gen_hash(password: str):
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256", 
        password=password.encode("utf-8"), 
        salt=os.urandom(32),
        iterations=20000
        )
    return key


class UserData(BaseModel):
    
    nickname: str = Field(
        min_length=3, max_length=64, kw_only=True
        )
    email_address: EmailStr = Field(
        strict=True, 
        pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        kw_only=True
        )
    password: bytes = Field(
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
    def get_all_users(cls) -> list:
        """Get a list of all users."""
        with cls.session.begin() as s:
            stmt = s.execute(select(cls.model)).scalars().all()
            users = [i.as_dict() for i in stmt]
            return users

    @classmethod
    def get_author_by_id(cls, user_id: int) -> dict|None:
        with cls.session.begin() as s:
            if user := (s.get(cls.model, user_id)):
                resp = user.as_dict()
            return resp if user else f"Not found user with id={user_id}"

    @classmethod    
    def delete_author(cls, user_id: int):
        with cls.session.begin() as s:
            if user := (s.get(cls.model, user_id)):
                try:
                    s.delete(user)
                    s.commit()
                    return "The data is deleted successfully."
                except exc.DatabaseError as e:
                    s.rollback()
                    return e._message()
            else:
                return "User with id={} not found.".format(user_id)

    @classmethod    
    def update_author(cls, user_id: int, new_data: dict):
        """Updates user data.
        
        Keyword arguments:
        user_id -- int
        new_data -- dict[str|str] with items:
            '{
            nickname: new_nickname
            email_address: new_email_address,
            password: new_password
            }'
        """
        
        with cls.session.begin() as s:
            try:
                ### TODO
                stmt = update(cls.model).where(cls.model.id == user_id).values(
                    nickname = new_data["nickname"],
                    email_address = new_data["email_address"],
                    password = gen_hash(new_data["password"])
                )
                s.execute(stmt)
                s.commit()
                return "The data is updated successfully."
            except exc.DatabaseError as e:
                s.rollback()
                return e._message()

    def is_exists(self, nickname: str, email_address: str):
        """Checking for a user database with 
        such nickname/email address."""
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
