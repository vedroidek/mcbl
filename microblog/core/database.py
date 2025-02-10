from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def engine(uri):
    return create_engine(
        uri,
        # echo=True,
        isolation_level="REPEATABLE READ", 
        pool_pre_ping=True
        )


def session():
    s = sessionmaker(engine)
    return s
