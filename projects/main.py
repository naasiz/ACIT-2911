from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from db.db import db
from models.models import User, Thread, Comment, Subheading, Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired

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
@main.route('/profile', methods=['GET','POST'])
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
            
# For updating user information
@main.route('/update<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = Form()
    name_to_update = db.get_or_404(User, id)
    if request.method == "POST":
        # print(form)
        # print(form.name)
        # print(form.email)
        print(request.form['name'])
        print(request.form['email'])
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            # flash("User Updated Successfully")
            # return render_template("update.html", form=form, name_to_update=name_to_update, user=current_user)
            return redirect(url_for('main.profile'))        
        except:
            db.session.commit()
            # flash("Error, there are problems, try again")
            return render_template("update.html", form=form, name_to_update=name_to_update,id=id, user=current_user)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update,id=id, user=current_user)





# @main.route('/update', methods=['GET', 'POST'])
# def update():
#     name = None
#     form = Form()
#     # Validate form
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ""
#     return render_template("update.html", name = name, form = form, user = current__user)
if __name__ == "__main__":
    main.run(debug=True)

# if __name__ == "__main__":
#     main.run(host='0.0.0.0', port=4000)