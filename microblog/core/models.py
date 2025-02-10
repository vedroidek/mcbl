from datetime import datetime, date
from typing import List, Annotated
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    relationship


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    
    __tablename__ = "user_account"

    id: Mapped[intpk]
    nickname: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False)
    email_address: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False)
    registered: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    person_data: Mapped["PersonData"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    posts: Mapped[List['Post']] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, fullname={self.nickname!r})"


class PersonData(Base):

    __tablename__ = "person_data"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    gender: Mapped[str]
    birthday: Mapped[date]
    user: Mapped["User"] = relationship(back_populates="personal_data")

    def __repr__(self) -> str:
        return f"PersonData(id={self.id!r}, \
            email_address={self.user.nickname!r})"
    

class Post(Base):

    __tablename__ = "post"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(128))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    comments_id: Mapped[List["Comment"]] = relationship(back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"


class Comment(Base):

    __tablename__ = "comment"

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    post_id: Mapped["Post"] = mapped_column(ForeignKey("post.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    author: Mapped["User"] = relationship(back_populates="comment")

    def __repr__(self):
        return f"Comment(id={self.id!r}, title={self.author.nickname!r})"