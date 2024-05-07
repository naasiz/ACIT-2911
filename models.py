from db import db 
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    threads = relationship("Thread")
    comments = relationship("Comment")
    
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         "name": self.name,
    #     }

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    title = db.Column(db.String(100))
    author = relationship("User", back_populates="threads")
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    comments = relationship("Comment")
    contetn = db.Column(db.String(1000))
    
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "user_id": self.user_id,
    #         "title": self.title,
    #         "author": self.author,
    #     }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=True)
    thread_id = mapped_column(Integer, ForeignKey(Thread.id), nullable=False)
    author = relationship("User", back_populates="comments")
    thread = relationship("Thread", back_populates="comments")
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    content = db.Column(db.String(1000))
    
    
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "phone": self.phone,
    #         "balance": self.balance,
    #     }
