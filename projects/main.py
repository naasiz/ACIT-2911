from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user 
from db.db import db
from models.models import User, Thread, Comment, Subheading

main = Blueprint('main', __name__)

# Main Routes
# For rendering forums.html
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

# For rendering profile.html
@main.route('/profile')
@login_required
def profile():
    return render_template('/auth/profile.html',  user=current_user)

# For rendering the thread_detailed.html
@main.route('/thread_detailed/<int:thread_id>')
def thread_detailed(thread_id):
    thread = db.get_or_404(Thread, thread_id)
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    try:
        if int(thread.author.id) == int(current_user.id):
            print(thread.author.id)
            print(current_user.id)
            return render_template("thread_detailed.html", thread = thread, user=current_user, edit = False, own = True)
        else:
            return render_template("thread_detailed.html", thread = thread, user=current_user, edit = False, own = False)
    except:
        return render_template("thread_detailed.html", thread = thread, user=current_user, edit = False, own = False)

@main.route('/thread_detailed/edit/<int:thread_id>')
def thread_edit(thread_id):
    thread = db.get_or_404(Thread, thread_id)
    thread.count = db.session.query(Comment).filter(Comment.thread_id == thread.id).count()
    return render_template("thread_detailed.html", thread = thread, user=current_user, edit = True)
   
# For rendering the add_thread.html
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

# For editing the thread 
@main.route("/thread_detailed/editing/<int:thread_id>", methods=["POST"])
def thread_update(thread_id):
    thread=db.get_or_404(Thread, thread_id)
    if request.form["title"] == "":
        return redirect(url_for('main.thread_detailed', thread_id=thread.id))
    thread.title=request.form["title"] 
    thread.content=request.form["content"] 
    db.session.commit()
    return redirect(url_for('main.thread_detailed', thread_id=thread.id))

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
        


