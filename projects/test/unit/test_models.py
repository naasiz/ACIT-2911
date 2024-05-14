from models.models import User, Subheading, Thread, Comment 
from werkzeug.security import generate_password_hash, check_password_hash

# Test the User model
def test_user():
    # Create a user object
    user = User(email="john@my.bcit.ca", password=generate_password_hash("password", method='pbkdf2:sha256'), name="John")
    
    # Assert the user object's attributes
    assert user.email == "john@my.bcit.ca"
    assert user.password != "password"
    
    # Check the password hash 
    assert check_password_hash(user.password, "password") == True

# Test the Subheading model
def test_subheading():
    subheading = Subheading(title="Test")
    assert subheading.title == "Test"

# Test the Thread 
def test_thread():
    thread = Thread(title="Test", content="Test")
    assert thread.title == "Test"
    assert thread.content == "Test"

# Test the Comment 
def test_comment():
    comment = Comment(content="Test")
    assert comment.content == "Test"