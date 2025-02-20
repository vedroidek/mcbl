from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DevelopmentConfig as DC


def engine(uri):
    return create_engine(
        uri,
        # echo=True,
        isolation_level="REPEATABLE READ", 
        pool_pre_ping=True
        )


def session():
    s = sessionmaker(engine(DC.DATABASE_URI), autoflush=True)
    return s
