from flask import Flask
from flask_login import LoginManager
from app.db import db
# from apps.manage import run
import os 
port = os.environ.get("PORT", 5000)
def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.main.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return db.get_or_404(User, user_id)

    # blueprint for auth routes in our app
    from app.main.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=port )
