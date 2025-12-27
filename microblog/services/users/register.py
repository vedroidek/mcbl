from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from microblog.models.user_models import User
from .security import check_password, hash_password


def register_new_user(
        session: Session,
        name: str,
        email: str,
        password: str) -> bool:
    """Register a new user in the database
    if not already taken.

    Check if a user with the given email
    address already exists in the database.

    Args:
        user: User object instance
    Returns:
        bool: True if registration was successful, False if user already exists
    *Note:*
        The user object will be committed to the database upon success.
    """
    is_success = False
    with session as s:
        stmt = select(exists().where(
            (User.email_address == email) |
            (User.name == name)
        ))
        if s.execute(stmt).scalar():
            return False

        try:
            password_hash = hash_password(password)
            user = User(name=name,
                        email_address=email,
                        password_hash=password_hash)
            s.add(user)
            s.commit()
            is_success = True
        except DatabaseError:
            return is_success
        finally:
            s.close()

    return is_success
