from main import app
from db import db
from models import User, Thread, Comment
from werkzeug.security import generate_password_hash, check_password_hash
import random


def create_User():
    db.session.add(User(email="tristanjames3131@gmail.com", password=generate_password_hash('Password', method='pbkdf2:sha256'), name="Tristan James Torres"))
    db.session.add(User(email="mmangilin22@my.bcit.ca", password=generate_password_hash('@Meriel2002', method='pbkdf2:sha256'), name="Meriel Mangilin"))
    db.session.commit()

def create_Thread(num):
    user =db.get_or_404(User, random.randint(1,2))
    db.session.add(Thread(author=user))
    db.session.commit()
    thread = db.get_or_404(Thread, num)
    thread.title = "What was your favourite course from term 1?"
    thread.content = "I really enjoyed COMP 1002, it was a great introduction to programming!"
    db.session.commit()
    
def delete_data():
    db.drop_all()

def create_comment():
    thread=db.get_or_404(Thread, 1)
    db.session.add(Comment(author=thread.author,thread=thread))
    db.session.commit()
    comment=db.get_or_404(Comment,1)
    comment.content = "SysAdmin was my favourite course!"
    db.session.commit()
      
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_User()
        create_Thread(1)
        create_comment()
