import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt with generated salt.

    Args:
        password (str): Plain text password to hash.

    Returns:
        str: Salted and hashed password as UTF-8 string.

    Example:
        hashed_password = hash_password("user_password")
    """

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash using constant-time comparison.

    Args:
        password (str): Plain text password to verify.
        hashed (str): Previously hashed password to compare against.

    Returns:
        bool: True if password matches hash, False otherwise.

    Example:
        is_valid = check_password("input_password", stored_hash)
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
