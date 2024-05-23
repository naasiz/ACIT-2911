from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user 
from db.db import db
from models.models import User, Thread, Comment, Subheading, Form, User_Thread_Upvotes
from datetime import datetime, date

main = Blueprint('main', __name__)

# Main Routes

# For rendering forums.html
@main.route('/')
def index():
    # Query the database to get all subheadings and order them by id
    statement = db.select(Subheading).order_by(Subheading.id)
    # Execute the query and convert the results to a list
    results = list(db.session.execute(statement).scalars())
    # Iterate over each subheading
    for subheading in results:
        # Iterate over each thread in the subheading
        for thread in subheading.threads:
            # Count the number of comments for each thread
            thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
            try:
                thread.upvotes = db.session.query(User_Thread_Upvotes).filter(User_Thread_Upvotes.thread_id == thread.id).count()
            except:
                thread.upvotes = 0
    try:
        # Render the forums.html template with the subheadings and current user
        return render_template('forums.html', subheadings=results, user=current_user)
    except AttributeError:
        # If there is no current user, render the forums.html template without the user
        return render_template('forums.html', subheadings=results)

# For rendering profile.html
@main.route('/profile')
@login_required
def profile():
    # Render the profile.html template with the current user
    return render_template('/auth/profile.html', user=current_user)

# For rendering the thread_detailed.html
@main.route('/thread_detailed/<int:thread_id>')
def thread_detailed(thread_id):
    # Get the thread with the specified thread_id from the database
    thread = db.get_or_404(Thread, thread_id)
    # Count the number of comments for the thread
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    try:
        # Check if the current user is the author of the thread
        if int(thread.author.id) == int(current_user.id):
            # Render the thread_detailed.html template with the thread, current user, and edit and own flags
            return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=True)
        else:
            # Render the thread_detailed.html template with the thread, current user, and edit and own flags
            return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=False)
    except:
        # Render the thread_detailed.html template with the thread, current user, and edit and own flags
        return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=False)

@main.route('/thread_detailed/edit/<int:thread_id>')
def thread_edit(thread_id):
    # Get the thread with the specified thread_id from the database
    thread = db.get_or_404(Thread, thread_id)
    # Count the number of comments for the thread
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    # Render the thread_detailed.html template with the thread, current user, and edit flag
    return render_template("thread_detailed.html", thread=thread, user=current_user, edit=True)

# For rendering the add_thread.html
@main.route('/add')
def add_page():
    # Query the database to get all subheadings and order them by id
    stmt = db.select(Subheading).order_by(Subheading.id)
    # Execute the query and convert the results to a list
    results = list(db.session.execute(stmt).scalars())
    # Render the add_thread.html template with the current user and subheadings
    return render_template("add_thread.html", user=current_user, subheadings=results)

# Post Routes
# For adding a thread
@main.route('/', methods=["POST"])
def add_thread():
    # Check if the content and title fields are not empty
    if request.form["content"] != "" and request.form["title"] != "":
        # Get the subheading with the specified subheading_id from the database
        subheading = db.get_or_404(Subheading, int(request.form["subheading"]))
        try:
            # Check if there is a current user
            user = db.get_or_404(User, current_user.id)
            # Create a new thread with the author, subheading, title, and content
            db.session.add(Thread(author=user, subheading=subheading, title=request.form["title"], content=request.form["content"]))
        except:
            # Create a new thread with the subheading, title, and content
            db.session.add(Thread(title=request.form["title"], subheading=subheading, content=request.form["content"]))
        # Commit the changes to the database
        db.session.commit()
        # Redirect to the index route
        return redirect(url_for('main.index'))
    else:
        # Flash an error message and redirect to the add_page route
        flash('Please check your title and content are not empty and try again.')
        return redirect(url_for('main.add_page'))

# For deleting thread
@main.route("/thread_detailed/delete/<int:thread_id>", methods=["POST"])
def del_thread(thread_id):
    # Get the thread with the specified thread_id from the database
    thread = db.get_or_404(Thread, thread_id)
    # Delete the thread from the database
    db.session.delete(thread)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the index route
    return redirect(url_for('main.index'))

# For editing the thread
@main.route("/thread_detailed/editing/<int:thread_id>", methods=["POST"])
def thread_update(thread_id):
    # Get the thread with the specified thread_id from the database
    thread = db.get_or_404(Thread, thread_id)
    # Check if the title field is not empty
    if request.form["title"] == "":
        # Redirect to the thread_detailed route
        return redirect(url_for('main.thread_detailed', thread_id=thread.id))
    # Update the title and content of the thread
    thread.title = request.form["title"]
    thread.content = request.form["content"]
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the thread_detailed route
    return redirect(url_for('main.thread_detailed', thread_id=thread.id))

# For adding comments
@main.route("/thread_detailed/<int:thread_id>", methods=["POST"])
def add_comment(thread_id):
    # Check if the content field is not empty
    if request.form["content"] != "":
        # Get the thread with the specified thread_id from the database
        thread = db.get_or_404(Thread, thread_id)
        try:
            # Check if there is a current user
            user = db.get_or_404(User, current_user.id)
            # Create a new comment with the author, thread, and content
            db.session.add(Comment(author=user, thread=thread, content=request.form["content"]))
        except AttributeError:
            # Create a new comment with the thread and content
            db.session.add(Comment(thread=thread, content=request.form["content"]))
        # Commit the changes to the database
        db.session.commit()
    # Redirect to the thread_detailed route
    return redirect(url_for('main.thread_detailed', thread_id=thread_id))

@main.route('/del/subheading/<int:subheading_id>', methods=["POST"])
def del_subheading(subheading_id):
    # Get the subheading with the specified subheading_id from the database
    subheading = db.get_or_404(Subheading, subheading_id)
    # Delete the subheading from the database
    db.session.delete(subheading)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the index route
    return redirect(url_for('main.index'))

@main.route('/del/comment/<int:comment_id>', methods=["POST"])
def del_comment(comment_id):
    # Get the comment with the specified comment_id from the database
    comment = db.get_or_404(Comment, comment_id)
    # Delete the comment from the database
    db.session.delete(comment)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the thread_detailed route
    return redirect(url_for('main.thread_detailed', thread_id=comment.thread_id))

@main.route('/update<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    # Create a new instance of the Form class
    form = Form()
    # Get the user with the specified id from the database
    name_to_update = db.get_or_404(User, id)
    if request.method == "POST":
        # Split the date_of_birth string into year, month, and day
        dateofbirth = request.form['date_of_birth'].split('-')
        year = int(dateofbirth[0])
        month = int(dateofbirth[1])
        day = int(dateofbirth[2])
        # Update the name, email, description, and date_of_birth of the user
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.description = request.form['description']
        name_to_update.date_of_birth = datetime(year, month, day).date()
        try:
            # Commit the changes to the database
            db.session.commit()
            # Redirect to the profile route
            return redirect(url_for('main.profile'))
        except:
            db.session.commit()
            # Render the update.html template with the form, name_to_update, id, and current user
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id, user=current_user)
    else:
        # Render the update.html template with the form, name_to_update, id, and current user
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id, user=current_user)
    
@main.route('/upvote', methods=['POST'])
def upvote():
    data = request.get_json()
    thread_id = data.get('thread_id')
    if thread_id:
        stmt = db.select(User_Thread_Upvotes).where(User_Thread_Upvotes.thread_id == thread_id).where(User_Thread_Upvotes.user_id == current_user.id)
        result = db.session.execute(stmt).scalar()
        db.session.add(User_Thread_Upvotes(thread_id=thread_id, user_id=current_user.id))
        action = 'added'
        db.session.commit()
        statement = db.select(User_Thread_Upvotes).where(User_Thread_Upvotes.thread_id == thread_id)
        resultt = db.session.execute(statement).scalars()
        count = len(list(resultt))
        return jsonify({'status': 'success', 'action': action, "upvotes": count})
    else:
        return jsonify({'status': 'error', 'message': 'No thread_id provided'}), 400
# @main.route('/upvote', methods=['POST'])
# def upvote():
#     data = request.get_json()
#     thread_id = data.get('thread_id')
#     if thread_id:
#         stmt = db.select(User_Thread_Upvotes).where(User_Thread_Upvotes.thread_id == thread_id).where(User_Thread_Upvotes.user_id == current_user.id)
#         result = db.session.execute(stmt).scalar()
#         if result is None:
#             db.session.add(User_Thread_Upvotes(thread_id=thread_id, user_id=current_user.id))
#             action = 'added'
#         else:
#             db.session.delete(result)
#             action = 'deleted'
#         db.session.commit()
#         statement = db.select(User_Thread_Upvotes).where(User_Thread_Upvotes.thread_id == thread_id)
#         resultt = db.session.execute(statement).scalars()
#         count = len(list(resultt))
#         return jsonify({'status': 'success', 'action': action, "upvotes": count})
#     else:
#         return jsonify({'status': 'error', 'message': 'No thread_id provided'}), 400
