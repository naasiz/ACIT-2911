from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from app.db import db
from app.main.models import User
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database to find the user
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Log the user in
            login_user(user)

            # Redirect to the root route
            return redirect(url_for('main.index'))  # replace 'index' with the actual endpoint for '/'

    # Render the login template and pass the current user object
    return render_template('/auth/login.html', user=current_user)

@auth.route('/signup')
def signup():
    # Render the signup template and pass the current user object
    return render_template('/auth/signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # Logout the user and redirect to the login page
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    # Get the email, password, and remember values from the form
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Query the database to find the user with the given email
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    # Check if the user exists and if the password is correct
    if not user or not check_password_hash(user.password, password):
        # Flash an error message and redirect to the login page
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    # Login the user and redirect to the profile page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    # Get the email, name, and password values from the form
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Check if any of the form fields are empty
    if email == "" or name == "" or password =="":
        # Flash an error message and redirect to the signup page
        flash("Do not leave form blank")
        return redirect(url_for('auth.signup'))

    # Query the database to find if the email already exists
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user:
        # Flash an error message and redirect to the signup page
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    # Create a new user with the form data and hash the password
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/users')
@login_required
def users():
    # Query the database to get all users except the one with id=1
    stmt=db.select(User).where(User.id != 1)
    results=db.session.execute(stmt).scalars()
    return render_template('/auth/list_users.html', users=results, user=current_user)

@auth.route('/users/delete/<int:id>', methods=["POST"])
@login_required
def del_user(id):
    # Check if the current user is not the admin (id=1)
    if current_user.id != 1:
        return redirect(url_for('main.index'))
    
    # Get the user with the given id from the database
    user=db.get_or_404(User, id)
    
    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.users'))