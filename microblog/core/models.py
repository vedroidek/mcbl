from datetime import date, datetime
from typing import Annotated, List

from sqlalchemy import ForeignKey, String, Text, func, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[intpk]
    nickname: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )
    password: Mapped[bytes] = mapped_column(LargeBinary(128), nullable=False)


class Author(Base):
    __tablename__ = "author_account"

    id: Mapped[intpk]
    nickname: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False)
    email_address: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary(128), nullable=False)
    registered: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    person_data: Mapped["PersonData"] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, nickname={self.nickname!r})"
    
    def as_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "registered": self.registered,
            "email_address": self.email_address,
            "person_data": self.person_data,
            "posts": self.posts,
            "comments": self.comments
        }


class PersonData(Base):
    __tablename__ = "person_data"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("author_account.id"))
    gender: Mapped[str]
    birthday: Mapped[date]
    author: Mapped["Author"] = relationship(back_populates="person_data")

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
    author_id: Mapped[int] = mapped_column(ForeignKey("author_account.id"))
    author: Mapped["Author"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("author_account.id"))
    author: Mapped["Author"] = relationship(back_populates="comments")

    def __repr__(self):
        return f"Comment(id={self.id!r}, title={self.author.nickname!r})"
