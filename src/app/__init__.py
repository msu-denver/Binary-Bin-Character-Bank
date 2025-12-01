from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Absolute path to templates in container
    template_folder = '/app/htmlcov'
    app = Flask(__name__, template_folder=template_folder)
    app.config['SECRET_KEY'] = 'DM for me'

    # Ensure database folder exists
    os.makedirs('/app/data', exist_ok=True)

    # SQLite database path
    db_path = '/app/data/CharacterBank.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'  # update for blueprint\

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprint
    from .routes import main
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
