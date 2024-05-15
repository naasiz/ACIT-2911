# from main import index, add_thread, del_thread, add_comment, login, signup, logout, login_post
from app import create_app
import pytest

@pytest.fixture
def client():
    return create_app().test_client()

@pytest.fixture
def runner():
    return create_app().test_cli_runner()

# Test the index route 
def test_index(client):
    response = client.get('/')
    response.content_type == 'text/html; charset=utf-8'
    print(response.data)
    assert response.status_code == 200