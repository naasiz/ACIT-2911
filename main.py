from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from db import db
from models import User, Thread, Comment

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # return User.query.get(int(user_id))
    return db.get_or_404(User, user_id)

# Main Routes
@app.route('/')
def main():
    statement=db.select(Thread).order_by(Thread.id)
    results=list(db.session.execute(statement).scalars())
    for thread in results:
        thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    
    try:    
        return render_template('main.html', threads=results, user=current_user)
    except AttributeError:
        return render_template('main.html', threads=results)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/thread_detailed/<int:thread_id>')
def thread_detailed(thread_id):
    thread = db.get_or_404(Thread, thread_id)
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    return render_template("thread_detailed.html", thread = thread)
    

# Post Routes
@app.route('/', methods=["POST"]) 
def add_thread():
    if request.form["content"] != "":
        try:
            user = db.get_or_404(User, current_user.id)
            db.session.add(Thread(author=user, title=request.form["content"]))
        except:
            db.session.add(Thread(title=request.form["content"]))
        db.session.commit()
    return redirect(url_for('main'))
    
@app.route("/thread_detailed/<int:thread_id>", methods=["POST"])
def add_comment(thread_id):
    thread = db.get_or_404(Thread, thread_id)
    try:
        user = db.get_or_404(User, current_user.id)
        db.session.add(Comment(author=user, thread=thread, content=request.form["content"]))
    except:
        db.session.add(Comment(thread=thread, content=request.form["content"]))
    db.session.commit()
    return redirect(url_for('thread_detailed', thread_id=thread_id))
    
# Auth Routes
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # user = User.query.filter_by(email=email).first()
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=8888)