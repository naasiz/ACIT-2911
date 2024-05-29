import pytest
from app.main.models import User, Subheading, Thread, Comment 
from werkzeug.security import generate_password_hash
from app import create_app

# Functional Test
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Unit Test
@pytest.fixture
def user_john():
    return User(email="john@my.bcit.ca", password=generate_password_hash("password", method='pbkdf2:sha256'), name="John")

@pytest.fixture
def subheading_test():
    return Subheading(title="Test")

@pytest.fixture
def thread_test(user_john, subheading_test):
    return Thread(author=user_john, subheading=subheading_test, title="Test", content="Test")

@pytest.fixture
def comment_test(user_john, thread_test):
    return Comment(author=user_john, thread=thread_test, content="Test")