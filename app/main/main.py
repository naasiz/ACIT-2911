from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user 
from app.db import db
from app.main.models import (
    User,
    Thread,
    Comment,
    Subheading,
    Form,
    User_Thread_Downvotes,
    User_Thread_Upvotes,
)
from datetime import datetime
from wtforms import TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import uuid as uuid
import os
main = Blueprint('main', __name__)  # Create a Blueprint object named 'main'

# Main Routes

@main.route("/")  # Route decorator for the index route
def index():
    try:
        if session["visited"] == "true":
            visited = "true"
    except KeyError:
        session["visited"] = "true"
        visited = "false"
    statement = db.select(Subheading).order_by(
        Subheading.id
    )  # Query the database to get all subheadings and order them by id
    results = list(
        db.session.execute(statement).scalars()
    )  # Execute the query and convert the results to a list
    for subheading in results:  # Iterate over each subheading
        for thread in subheading.threads:  # Iterate over each thread in the subheading
            thread.count = (
                db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
            )  # Count the number of comments for each thread
            try:
                thread.upvotes = (
                    db.session.query(User_Thread_Upvotes)
                    .filter(User_Thread_Upvotes.thread_id == thread.id)
                    .count()
                )  # Count the number of upvotes for each thread
                thread.upvoted = (
                    db.session.query(User_Thread_Upvotes)
                    .filter(User_Thread_Upvotes.thread_id == thread.id)
                    .filter(User_Thread_Upvotes.user_id == current_user.id)
                    .count()
                )  # Check if the current user has upvoted the thread
            except:
                thread.upvotes = (
                    db.session.query(User_Thread_Upvotes)
                    .filter(User_Thread_Upvotes.thread_id == thread.id)
                    .count()
                )  # Count the number of upvotes for each thread

            try:
                thread.downvotes = (
                    db.session.query(User_Thread_Downvotes)
                    .filter(User_Thread_Downvotes.thread_id == thread.id)
                    .count()
                )  # Count the number of downvotes for each thread
                thread.downvoted = (
                    db.session.query(User_Thread_Downvotes)
                    .filter(User_Thread_Downvotes.thread_id == thread.id)
                    .filter(User_Thread_Downvotes.user_id == current_user.id)
                    .count()
                )  # Check if the current user has downvoted the thread
            except:
                thread.downvotes = (
                    db.session.query(User_Thread_Downvotes)
                    .filter(User_Thread_Downvotes.thread_id == thread.id)
                    .count()
                )  # Count the number of downvotes for each thread
    try:
        return render_template(
            "index.html", subheadings=results, user=current_user, visited=visited
        )  # Render the index.html template with the subheadings and current user
    except AttributeError:
        return render_template(
            "index.html", subheadings=results, visited=visited
        )  # If there is no current user, render the index.html template without the user

@main.route('/profile')  # Route decorator for the profile route
@login_required  # Require login to access the profile route
def profile():
    # stmt = db.select(User_Thread_Upvotes).where(User_Thread_Upvotes.user_id == current_user.id)  # Check if the current user has upvoted the thread
    # posts = len(list(db.session.execute(stmt).scalars()))
    posts = len(list(current_user.threads))
    comments = len(list(current_user.comments))
    return render_template('/auth/profile.html', user=current_user, posts=posts, comments=comments)  # Render the profile.html template with the current user

@main.route('/thread_detailed/<int:thread_id>')  # Route decorator for the thread_detailed route
def thread_detailed(thread_id):
    thread = db.get_or_404(Thread, thread_id)  # Get the thread with the specified thread_id from the database
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()  # Count the number of comments for the thread
    # try:
    #     if int(thread.author.id) == int(current_user.id):  # Check if the current user is the author of the thread
    #         return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=True)  # Render the thread_detailed.html template with the thread, current user, and edit and own flags
    #     else:
    #         return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=False)  # Render the thread_detailed.html template with the thread, current user, and edit and own flags
    # except:
    #     return render_template("thread_detailed.html", thread=thread, user=current_user, edit=False, own=False)  # Render the thread_detailed.html template with the thread, current user, and edit and own flags
    if current_user.is_authenticated:
        # if using login account, allow to have ability to edit thread and comment (Just ability, specifically when they can use will be on different function)
        return render_template("thread_detailed.html", thread=thread, edit=False, edit_comment_id = None)
    else:
        # if not login, just be able to access to thread_detailed.html
        return render_template("thread_detailed.html", thread=thread)

@main.route('/thread_detailed/edit/<int:thread_id>')  # Route decorator for the thread_edit route
def thread_edit(thread_id):
    thread = db.get_or_404(Thread, thread_id)  # Get the thread with the specified thread_id from the database
    if current_user.id == thread.author.id:
        # if users own that thread, allow edit
        thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()  # Count the number of comments for the thread
        return render_template("thread_detailed.html", thread=thread, user=current_user, edit=True, edit_comment_id=None)  # Render the thread_detailed.html template with the thread, current user, and edit flag
    else:
        # if not own thread, just allow to see as non-login user, redirect to thread_detailed.html
        return redirect(url_for("main.thread_detailed", thread_id=thread.id))

@main.route('/add')  # Route decorator for the add_page route
def add_page():
    stmt = db.select(Subheading).order_by(Subheading.id)  # Query the database to get all subheadings and order them by id
    results = list(db.session.execute(stmt).scalars())  # Execute the query and convert the results to a list
    return render_template("add_thread.html", user=current_user, subheadings=results)  # Render the add_thread.html template with the current user and subheadings

# Post Routes

@main.route('/', methods=["POST"])  # Route decorator for the add_thread route
def add_thread():
    if request.form["content"] != "" and request.form["title"] != "":  # Check if the content and title fields are not empty
        subheading = db.get_or_404(Subheading, int(request.form["subheading"]))  # Get the subheading with the specified subheading_id from the database
        try:
            user = db.get_or_404(User, current_user.id)  # Check if there is a current user
            db.session.add(Thread(author=user, subheading=subheading, title=request.form["title"], content=request.form["content"]))  # Create a new thread with the author, subheading, title, and content
        except:
            db.session.add(Thread(title=request.form["title"], subheading=subheading, content=request.form["content"]))  # Create a new thread with the subheading, title, and content
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('main.index'))  # Redirect to the index route
    else:
        flash('Please check your title and content are not empty and try again.')  # Flash an error message
        return redirect(url_for('main.add_page'))  # Redirect to the add_page route

@main.route("/thread_detailed/delete/<int:thread_id>", methods=["POST"])  # Route decorator for the del_thread route
def del_thread(thread_id):
    thread = db.get_or_404(Thread, thread_id)  # Get the thread with the specified thread_id from the database
    db.session.delete(thread)  # Delete the thread from the database
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.index'))  # Redirect to the index route

@main.route("/thread_detailed/editing/<int:thread_id>", methods=["POST"])  # Route decorator for the thread_update route
def thread_update(thread_id):
    thread = db.get_or_404(Thread, thread_id)  # Get the thread with the specified thread_id from the database
    if request.form["title"] == "":  # Check if the title field is not empty
        return redirect(url_for('main.thread_detailed', thread_id=thread.id))  # Redirect to the thread_detailed route
    thread.title = request.form["title"]  # Update the title and content of the thread
    thread.content = request.form["content"]
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.thread_detailed', thread_id=thread.id))  # Redirect to the thread_detailed route

@main.route("/thread_detailed/<int:thread_id>", methods=["POST"])  # Route decorator for the add_comment route
def add_comment(thread_id):
    if request.form["content"] != "":  # Check if the content field is not empty
        thread = db.get_or_404(Thread, thread_id)  # Get the thread with the specified thread_id from the database
        try:
            user = db.get_or_404(User, current_user.id)  # Check if there is a current user
            db.session.add(Comment(author=user, thread=thread, content=request.form["content"]))  # Create a new comment with the author, thread, and content
        except AttributeError:
            db.session.add(Comment(thread=thread, content=request.form["content"]))  # Create a new comment with the thread and content
        db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.thread_detailed', thread_id=thread_id))  # Redirect to the thread_detailed route

@main.route('/del/subheading/<int:subheading_id>', methods=["POST"])  # Route decorator for the del_subheading route
def del_subheading(subheading_id):
    subheading = db.get_or_404(Subheading, subheading_id)  # Get the subheading with the specified subheading_id from the database
    db.session.delete(subheading)  # Delete the subheading from the database
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.index'))  # Redirect to the index route

@main.route('/del/comment/<int:comment_id>', methods=["POST"])  # Route decorator for the del_comment route
def del_comment(comment_id):
    comment = db.get_or_404(Comment, comment_id)  # Get the comment with the specified comment_id from the database
    db.session.delete(comment)  # Delete the comment from the database
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.thread_detailed', thread_id=comment.thread_id))  # Redirect to the thread_detailed route

@main.route('/update<int:id>', methods=['GET', 'POST'])  # Route decorator for the update route
@login_required  # Require login to access the update route
def update(id):
    form = Form()  # Create a new instance of the Form class
    class From(FlaskForm):
        description = TextAreaField("Description", validators=[DataRequired()], default=f"{current_user.description}")

    form_two = From()    
    name_to_update = db.get_or_404(User, id)  # Get the user with the specified id from the database
    if request.method == "POST":
        dateofbirth = request.form['date_of_birth'].split('-')  # Split the date_of_birth string into year, month, and day
        year = int(dateofbirth[0])
        month = int(dateofbirth[1])
        day = int(dateofbirth[2])
        name_to_update.name = request.form['name']  # Update the name, email, description, and date_of_birth of the user
        name_to_update.email = request.form['email']
        name_to_update.description = request.form['description']
        name_to_update.date_of_birth = datetime(year, month, day).date()
        try:
            db.session.commit()  # Commit the changes to the database
            return redirect(url_for('main.profile'))  # Redirect to the profile route
        except:
            db.session.commit()
            return render_template("update.html", form=form, form_two=form_two, name_to_update=name_to_update, id=id, user=current_user)  # Render the update.html template with the form, name_to_update, id, and current user
    else:
        return render_template("update.html", form=form, form_two=form_two, name_to_update=name_to_update, id=id, user=current_user)  # Render the update.html template with the form, name_to_update, id, and current user

@main.route("/upvote", methods=["POST"])  # Route decorator for the upvote route
@login_required
def upvote():
    data = request.get_json()
    thread_id = data.get("thread_id")
    if thread_id:
        stmt = (
            db.select(User_Thread_Upvotes)
            .where(User_Thread_Upvotes.thread_id == thread_id)
            .where(User_Thread_Upvotes.user_id == current_user.id)
        )  # Check if the current user has upvoted the thread
        result = db.session.execute(stmt).scalar()
        if result is None:
            db.session.add(
                User_Thread_Upvotes(thread_id=thread_id, user_id=current_user.id)
            )  # Add upvote to the thread
            db.session.commit()
        else:
            db.session.delete(result)  # Remove upvote from the thread
            db.session.commit()

        statement = db.select(User_Thread_Upvotes).where(
            User_Thread_Upvotes.thread_id == thread_id
        )  # Query the database to get all upvotes for the thread
        result = db.session.execute(statement).scalars()
        count = len(list(result))  # Count the number of upvotes
        return jsonify(
            {"status": "success", "upvotes": count}
        )  # Return success status and the number of upvotes
    else:
        return (
            jsonify({"status": "error", "message": "No thread_id provided"}),
            400,
        )  # Return error status if no thread_id is provided


@main.route("/downvote", methods=["POST"])  # Route decorator for the downvote route
@login_required
def downvote():
    data = request.get_json()
    thread_id = data.get("thread_id")
    if thread_id:
        stmt = (
            db.select(User_Thread_Downvotes)
            .where(User_Thread_Downvotes.thread_id == thread_id)
            .where(User_Thread_Downvotes.user_id == current_user.id)
        )  # Check if the current user has downvoted the thread
        result = db.session.execute(stmt).scalar()
        if result is None:
            db.session.add(
                User_Thread_Downvotes(thread_id=thread_id, user_id=current_user.id)
            )  # Add down to the thread
            db.session.commit()
        else:
            db.session.delete(result)  # Remove downvote from the thread
            db.session.commit()

        statement = db.select(User_Thread_Downvotes).where(
            User_Thread_Downvotes.thread_id == thread_id
        )  # Query the database to get all downvotes for the thread
        result = db.session.execute(statement).scalars()
        count = len(list(result))  # Count the number of downvotes
        return jsonify(
            {"status": "success", "downvotes": count}
        )  # Return success status and the number of downvotes
    else:
        return (
            jsonify({"status": "error", "message": "No thread_id provided"}),
            400,
        )  # Return error status if no thread_id is provided


@main.route("/comment_reply/<int:comment_id>", methods=["POST"])  # Route decorator for the add_reply route
def add_reply(comment_id):
    parent_comment = db.get_or_404(Comment, comment_id)  # Get the parent comment with the specified comment_id from the database
    if request.form["content"] != "":  # Check if the content field is not empty
        try:
            user = db.get_or_404(User, current_user.id)  # Check if there is a current user
            db.session.add(Comment(author=user, thread=parent_comment.thread, content=request.form["content"], parent_id=parent_comment.id))  # Create a new reply with the author, thread, content, and parent_id
        except AttributeError:
            db.session.add(Comment(thread=parent_comment.thread, content=request.form["content"], parent_id=parent_comment.id))  # Create a new reply with the thread, content, and parent_id
        db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.thread_detailed', thread_id=parent_comment.thread.id)) # redirect to thread_detailed.html

    
@main.route('/edit/<int:comment_id>')  # Route decorator for the comment_edit route
def comment_edit(comment_id):
    comment = db.get_or_404(Comment, comment_id)  # Get the comment with the specified comment_id from the database
    comment.count = db.session.query(Comment).filter(Comment.parent_id == comment.id).count()  # Count the number of replies for the comment
    thread = comment.thread  # Get the thread that the comment belongs to
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()  # Count the number of comments for the thread
    return render_template("thread_detailed.html", thread=thread, comment=comment, user=current_user, edit_comment_id=comment_id)  # Render the thread_detailed.html template with the thread, comment, current user, and edit flag

@main.route("/update/<int:comment_id>", methods=["POST"])  # Route decorator for the comment_update route
def comment_update(comment_id):
    comment = db.get_or_404(Comment, comment_id)  # Get the comment with the specified comment_id from the database
    if request.form["content"] == "":  # Check if the content field is not empty
        return redirect(url_for('main.thread_detailed', thread_id=comment.thread.id))  # Redirect to the thread_detailed route
    comment.content = request.form["content"]  # Update the content of the comment
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('main.thread_detailed', thread_id=comment.thread.id))  # Redirect to the thread_detailed route

