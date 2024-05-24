from app import create_app 
from db.db import db
from datetime import datetime, date  
from models.models import User, Thread, Comment, Subheading
from werkzeug.security import generate_password_hash
import random
from faker import Faker
fake=Faker()

def create_User():
    db.session.add(User(email="tristanjames3131@gmail.com", password=generate_password_hash('Password', method='pbkdf2:sha256'), name="Tristan James Torres", description="I am a student at BCIT studying Computer Information Technology.", date_of_birth=datetime(2002, 7, 31).date(), profile_pic="./static/Default-user-icon.svg"))
    db.session.add(User(email="mmangilin22@my.bcit.ca", password=generate_password_hash('Password', method='pbkdf2:sha256'), name="Meriel Mangilin", description="I am a student at BCIT studying Computer Information Technology.", date_of_birth=datetime(2002, 2, 22).date(), profile_pic="./static/Default-user-icon.svg"))
    for _ in range(30):
        email = f"user{_}@example.com"
        name = f"User {_}"
        description = "I am a user."
        date_of_birth = datetime(2000, 1, 1).date()
        profile_pic = "./static/Default-user-icon.svg"
        user = User(email=email, password=generate_password_hash('Password', method='pbkdf2:sha256'), name=name, description=description, date_of_birth=date_of_birth, profile_pic = profile_pic)
        db.session.add(user)
    db.session.commit()

def create_Thread():
    db.session.add(Subheading(title="General Discussion"))                              
    db.session.add(Subheading(title="ACIT1630"))                              
    db.session.add(Subheading(title="MATH1200"))                              
    db.session.add(Subheading(title="COMM1430"))                              
    db.session.commit()
    
    def thread_return(user, subhead):
        title = fake.sentence(nb_words=6)
        content = fake.text(max_nb_chars=200)
        return Thread(author=user, subheading=subhead, title=title, content=content)
    
    for i in range(2, 34):
        user =db.get_or_404(User, random.randint(2,3))
        subheading =db.get_or_404(Subheading, random.randint(1,4))
        thread = thread_return(user, subheading)
        db.session.add(thread)
        db.session.commit()
    
def create_comment(parent_id=None):
    thread=db.get_or_404(Thread, 1)
    print(f"Thread: {thread}")  # print the thread object
    print(f"Thread ID: {thread.id}")  # print the thread id
    db.session.add(Comment(author=thread.author,thread=thread, thread_id=thread.id, parent_id=parent_id))
    db.session.commit()
    comment=db.get_or_404(Comment,1)
    comment.content = "SysAdmin was my favourite course!"
    db.session.commit()

def create_admin():
    admin=User(name="Admin", email="Admin@gmail.com", password=generate_password_hash('Password', method='pbkdf2:sha256'))
    db.session.add(admin)
    db.session.commit()
    
def run():
    with create_app().app_context():
        db.drop_all()
        db.create_all()
        create_admin()
        create_User()
        create_Thread()
        create_comment()     
        
if __name__ == "__main__":
    run()
    print('manage.py completed')
