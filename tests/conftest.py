from sqlalchemy.orm import sessionmaker
from . import pytest, models, create_engine, insert, select
from microblog.core import create_app, initial_db, drop_db
from microblog.config import TestingConfig


@pytest.fixture(scope="module")
def app():
    app = create_app(TestingConfig)
    initial_db(TestingConfig.dsn())
    yield app
    drop_db(TestingConfig.dsn())


@pytest.fixture
def session():
    engine = create_engine(
        TestingConfig.dsn(),
        # echo=True,
        isolation_level="REPEATABLE READ", 
        pool_pre_ping=True
        )
    s = sessionmaker(engine, autoflush=True)
    return s


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module")
def correct_user_data() -> dict[str:str]:
    return {
        "nickname": "some_user",
        "email_address": "some_user@mail.tu",
        "password": "some_password"
    }


@pytest.fixture
def create_user(session, correct_user_data):
    with session.begin() as s:
        s.add(models.Author(**correct_user_data))
        s.commit()
        return True
