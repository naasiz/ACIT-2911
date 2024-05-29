import pytest
from app.main.models import User, Subheading, Thread, Comment 
from werkzeug.security import generate_password_hash, check_password_hash

# Test the User model
def test_user(user_john):
    # Assert the user object's attributes
    assert user_john.email == "john@my.bcit.ca"
    assert user_john.password != "password"

    # Check the password hash 
    assert check_password_hash(user_john.password, "password") == True

# Test the Subheading model
def test_subheading(subheading_test):
    assert subheading_test.title == "Test"

# Test the Thread 
def test_thread(thread_test):
    assert thread_test.content == "Test"
    assert thread_test.title == "Test"

# Test the Comment 
def test_comment(comment_test):
    assert comment_test.content == "Test"
    

# Relationship between the models are tested

# Test the relationship between User and Thread
def test_user_thread(user_john, thread_test):
    # Create a thread object and add it to the user's threads
    assert user_john.threads[0].title == "Test"
def test_user_no_thread(user_john):
    # Create a user without threads
    assert len(user_john.threads) == 0

# Test the relationship between User and Comment
def test_user_comment(user_john, comment_test):
    # Create a comment object and add it to the user's comments
    assert user_john.comments[0].content == "Test"
def test_user_no_comment(user_john):
    # Create a user without comments
    assert len(user_john.comments) == 0

# Test the relationship between Thread and Comment
def test_thread_comment(thread_test, comment_test):
    # Create a comment object and add it to the thread's comments
    assert thread_test.comments[0].content == "Test"
def test_thread_no_comment(thread_test):
    # Create a thread without comments
    assert len(thread_test.comments) == 0