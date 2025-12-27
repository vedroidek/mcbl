from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from microblog.models.user_models import User


def get_all_users(session: Session) -> Sequence:
    stmt = select(User)
    with session as s:
        query = s.scalars(stmt).all()
    return [user.as_dict() for user in query] if query else []


def get_one_user(session: Session, id: int) -> User | None:
    with session as s:
        user = s.get(User, id)
    return user if user else None


def delete_one_user(session: Session, id: int) -> bool:
    is_success = False
    with session as s:
        if user := get_one_user(session, id):
            s.delete(user)
            s.commit()
            is_success = True
    return is_success