from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



# create the extension
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # create the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a very secret key 123'
    # configure the SQLite database, relative to the app instance folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialize the app with the extension
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    # If you define models in other modules, you must import them before calling create_all, otherwise SQLAlchemy will not know about them.
    from .models import User, Note
    # Create the Tables if they does not exist
    with app.app_context():
        db.create_all() 



    # initialize de login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where to redirect if login is not done
    login_manager.init_app(app) # connect to the app

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


