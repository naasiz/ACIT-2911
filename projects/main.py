from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from db.db import db
from models.models import User, Thread, Comment, Subheading

main = Blueprint('main', __name__)


# Main Routes
# For rendering all the threads
@main.route('/')
def index():
    statement=db.select(Subheading).order_by(Subheading.id)
    results=list(db.session.execute(statement).scalars())
    for subheading in results:
        for thread in subheading.threads:
            thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    try:    
        return render_template('forums.html', subheadings=results, user=current_user)
    except AttributeError:
        return render_template('forums.html', subheadings=results)

# For rending the currently logged in profile page
@main.route('/profile')
@login_required
def profile():
    return render_template('/auth/profile.html',  user=current_user)

# For rending the thread's comments
@main.route('/thread_detailed/<int:thread_id>')
def thread_detailed(thread_id):
    thread = db.get_or_404(Thread, thread_id)
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    return render_template("thread_detailed.html", thread = thread, user=current_user)
    
# For rending the add page
@main.route('/add')
def add_page():
    stmt = db.select(Subheading).order_by(Subheading.id)
    results=list(db.session.execute(stmt).scalars())
    return render_template("add_thread.html", user=current_user, subheadings=results)

# Post Routes
# For adding a thread 
@main.route('/', methods=["POST"]) 
def add_thread():
    if request.form["content"] != "" and request.form["title"] != "":
        subheading = db.get_or_404(Subheading, int(request.form["subheading"]))
        try:
            user = db.get_or_404(User, current_user.id)
            db.session.add(Thread(author=user, subheading=subheading, title=request.form["title"], content=request.form["content"]))
        except:
            db.session.add(Thread(title=request.form["title"], subheading=subheading, content=request.form["content"]))
        db.session.commit()
        return redirect(url_for('main.index'))
    else: 
        flash('Please check your title and content are not empty and try again.')    
        return redirect(url_for('main.add_page'))
 
# For deleting thread
@main.route("/thread_detailed/delete/<int:thread_id>", methods=["POST"])
def del_thread(thread_id):
    thread=db.get_or_404(Thread, thread_id)
    db.session.delete(thread)
    db.session.commit()
    return redirect(url_for('main.index'))

# For adding comments   
@main.route("/thread_detailed/<int:thread_id>", methods=["POST"])
def add_comment(thread_id):
    if request.form["content"] != "":
        thread = db.get_or_404(Thread, thread_id)
        try:
            user = db.get_or_404(User, current_user.id)
            db.session.add(Comment(author=user, thread=thread, content=request.form["content"]))
        except AttributeError:
            db.session.add(Comment(thread=thread, content=request.form["content"]))
        db.session.commit()
    return redirect(url_for('main.thread_detailed', thread_id=thread_id))
            
# Auth Routes
@main.route('/login')
def login():
    return render_template('/auth/login.html', user=current_user)

@main.route('/signup')
def signup():
    return render_template('/auth/signup.html', user=current_user)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@main.route('/login', methods=['POST'])
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
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))

@main.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@main.route('/homepage')
def toHome():
    return render_template('homepage-file/homepage.html')

@main.route('/posts')
def posts():
    threads = db.session.query(Thread).order_by(Thread.id).all()
    for thread in threads:
        thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    user = current_user if current_user.is_authenticated else None  # Assuming you're using Flask-Login
    return render_template('homepage-file/posts.html', threads=threads, user=user)

@main.route('/add_comment/<int:thread_id>', methods=["POST"])
def add_posts(thread_id):
    content = request.form["content"]
    if content:
        try:
            user = db.get_or_404(User, current_user.id)
            thread = db.session.query(Thread).get(thread_id)
            db.session.add(Comment(author=user, thread=thread, content=content))
        except:
            thread = db.session.query(Thread).get(thread_id)
            db.session.add(Comment(thread=thread, content=content))
        db.session.commit()
    return redirect(url_for('main.posts'))


@main.route('/upvote', methods=['POST'])
def upvote():
    thread_id = request.form.get('thread_id')
    # Update the upvote count in the database for the specified thread_id
    # Return the updated count
    return jsonify({'upvotes': 5})

@main.route('/downvote', methods=['POST'])
def downvote():
    thread_id = request.form.get('thread_id')
    # Update the downvote count in the database for the specified thread_id
    # Return the updated count
    return jsonify({'downvotes': 5})

if __name__ == "__main__":
    main.run(debug=True)

# if __name__ == "__main__":
#     main.run(host='0.0.0.0', port=4000)~