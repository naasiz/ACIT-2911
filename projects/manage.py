from app import create_app 
from db.db import db
from models.models import User, Thread, Comment, Subheading
from werkzeug.security import generate_password_hash
import random


def create_User():
    db.session.add(User(email="tristanjames3131@gmail.com", password=generate_password_hash('Password', method='pbkdf2:sha256'), name="Tristan James Torres", description="I am a student at BCIT studying Computer Systems Technology."))
    db.session.add(User(email="mmangilin22@my.bcit.ca", password=generate_password_hash('@Meriel2002', method='pbkdf2:sha256'), name="Meriel Mangilin", description="I am a student at BCIT studying Computer Systems Technology."))
    db.session.commit()

def create_Thread():
    db.session.add(Subheading(title="General Discussion"))                              
    db.session.add(Subheading(title="ACIT1630"))                              
    db.session.add(Subheading(title="MATH1200"))                              
    db.session.add(Subheading(title="COMM1430"))                              
    db.session.commit()
    def thread_return(i, user, subhead):
        if i == 0:
           thread = Thread(author=user, subheading=subhead, title="What was your favourite course from term 1?", content="I really enjoyed COMP 1002, it was a great introduction to programming!")
        elif i == 1:
           thread = Thread(author=user, subheading=subhead, title="Favourite project??", content="I really enjoyed COMP 1002, it was a great introduction to programming!")
        elif i == 2:
           thread = Thread(author=user, subheading=subhead, title="MATH1200 is pretty easy!", content="I really enjoyed COMP 1002, it was a great introduction to programming!")
        elif i == 3:
           thread = Thread(author=user, subheading=subhead, title="Headings, Bulleted Lists Blah Blah", content="I really enjoyed COMP 1002, it was a great introduction to programming!")
        
        return thread
    
    for i in range(1, 5):
        user =db.get_or_404(User, random.randint(1,2))
        subheading =db.get_or_404(Subheading, i)
        thread = thread_return(i-1,user, subheading)
        db.session.add(thread)
        db.session.commit()
    
def create_comment():
    thread=db.get_or_404(Thread, 1)
    db.session.add(Comment(author=thread.author,thread=thread))
    db.session.commit()
    comment=db.get_or_404(Comment,1)
    comment.content = "SysAdmin was my favourite course!"
    db.session.commit()

def run():
    with create_app().app_context():
        db.drop_all()
        db.create_all()
        create_User()
        create_Thread()
        create_comment()     
        
if __name__ == "__main__":
    run()
    print('manage.py completed')
