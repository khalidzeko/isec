from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # to manage the logged in user

# setup database:
db = SQLAlchemy()
db_name = "database.db"
# then configure it down 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'THIS IS A RNADOM  SECRET KEY' # to protect the cookies & sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    #Register what's on the view.py def
    from .view import view
    from .auth import auth
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #create database:
    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where user should go if not logged in 
    login_manager.init_app(app) # tell flask which app we use
    @login_manager.user_loader
    def load_user(id): # 
        return User.query.get(int(id)) # how load user to login, by id which by the primery key

    return app


#create database if not exists:
def create_database(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
        print('Created Database!')
