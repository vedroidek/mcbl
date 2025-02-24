from . import pytest, models, select


@pytest.mark.parametrize(
        ("data", "expected"),
        [
            ({
            "nickname": "TestUser",
            "email_address": "test_email@mail.tu",
            "password": "test_password"
            }, 201),
            ({
            "nickname": "TestUser",
            "email_address": "",
            "password": "test_password"
            }, 400),
            ({
            "nickname": "TestUser",
            "email_address": "test_email@mail",
            "password": "test_password"
            }, 400),
            ({
            "nickname": "TestUser2",
            "email_address": "test_emailmail.tu",
            "password": "test_password"
            }, 400),
            ({"nickname": "TestUser",
            "email_address": "test_email@mail.tu",
            "password": ""
            }, 400),
            ({
            "nickname": "",
            "email_address": "test_email@mail.tu",
            "password": "test_password"
            }, 400)
        ]
)
def test_register_post(client, data, expected):
    for i in data:
        response = client.post("/user/register", json=data)
        assert response.status_code == 200
        assert response.json["status_code"] == expected

@pytest.mark.parametrize(
        ("data", "expected"),
        [
            ({
            "nickname": "TestUser",
            "email_address": "test_email@mail.tu",
            "password": "test_password"
            }, 401),
            ({
            "nickname": "TestUser",
            "email_address": "",
            "password": "test_password"
            }, 401),
            ({
            "nickname": "TestUser",
            "email_address": "test_email@mail",
            "password": "test_password"
            }, 401),
            ({
            "nickname": "TestUser2",
            "email_address": "test_emailmail.tu",
            "password": "test_password"
            }, 401),
            ({"nickname": "TestUser",
            "email_address": "test_email@mail.tu",
            "password": ""
            }, 401),
            ({
            "nickname": "",
            "email_address": "test_email@mail.tu",
            "password": "test_password"
            }, 401)
        ]
)
def test_register_get(client, data, expected):
    for i in data:
        response = client.get("/user/register", json=data)
        assert response.status_code == expected


def test_get_test_user(session, correct_user_data, create_user):
    with session.begin() as s:
        stmt = select(models.Author).where(
            models.Author.nickname == correct_user_data["nickname"]
            )
        user = s.execute(stmt)
        assert user.scalar().nickname == correct_user_data["nickname"]

