from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config
from datetime import datetime
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

        @app.context_processor
        def inject_globals():
            return {'current_year': datetime.now().year}

    return app

def allowed_file(filename):
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']