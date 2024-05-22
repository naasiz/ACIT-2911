from db.db import db 
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    threads = relationship("Thread")
    comments = relationship("Comment")
    
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

# Create a class Form
class Form(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    description = TextAreaField("Description")
    
    submit = SubmitField("Submit")
    


