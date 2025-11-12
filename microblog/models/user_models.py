from datetime import datetime
from sqlalchemy import String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class User(Base):
    """
    *User model representing a system user account.*

    ### Stores basic user information including identification and
    ### contact details.

    :param name: User's name, max 32 characters
    :param email_address: User's email address, max 64 characters
    :param password: User's password, max 128 characters

    *Example*:
    ```python
    user = User(
        name='Neo',
        email_address='white_rabbit@matrix.fut',
        password='qwerty123')
    ```
    """

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email_address: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False
        )
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint('name', 'email_address', name='uq_user_name_email'),
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r},\nname={self.name!r}, \
        registered_at={self.registered_at!r})\n\n"
