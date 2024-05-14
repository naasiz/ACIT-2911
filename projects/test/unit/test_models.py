from models.models import User, Subheading, Thread, Comment 
from werkzeug.security import generate_password_hash, check_password_hash


# Test the User model
def test_user():
    user = User(email="john@my.bcit.ca", password=generate_password_hash("password", method='pbkdf2:sha256'), name="John")
    assert user.email == "john@my.bcit.ca"
    assert user.password != "password"