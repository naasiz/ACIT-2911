from app.db import db 
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    date_of_birth = db.Column(db.Date)
    threads = relationship("Thread", cascade="all, delete")
    comments = relationship("Comment", cascade="all, delete")
    profile_pic = db.Column(db.String(), nullable=True)


class Subheading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threads = relationship("Thread", cascade="all, delete")
    title = db.Column(db.String(1000), unique=True)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    subheading_id = mapped_column(Integer, ForeignKey(Subheading.id), nullable=True)
    title = db.Column(db.String(100), unique=True)
    author = relationship("User", back_populates="threads")
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    comments = relationship("Comment", cascade="all, delete")
    subheading = relationship("Subheading", back_populates="threads")
    content = db.Column(db.String(1000))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    thread_id = mapped_column(Integer, ForeignKey(Thread.id), nullable=False)
    author = relationship("User", back_populates="comments")
    thread = relationship("Thread", back_populates="comments")
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String(1000))
    # For replies
    parent_id = mapped_column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', cascade="all, delete", backref=db.backref('parent', remote_side=[id]), lazy='dynamic')  # new field for replies
    @property
    def depth(self):
        depth = 0
        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent
        return depth


class User_Thread_Upvotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    thread_id = mapped_column(Integer, ForeignKey(Thread.id), nullable=True)
    user = relationship("User")
    thread = relationship("Thread")


class User_Thread_Downvotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    thread_id = mapped_column(Integer, ForeignKey(Thread.id), nullable=True)
    user = relationship("User")
    thread = relationship("Thread")


# Create a class Form
class Form(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    date_of_birth = DateField("Date of Birth")
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")
    

