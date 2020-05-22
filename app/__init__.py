from flask import Flask
from config import TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(TestConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from app import routes, models

# Register Blueprints
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from app.solve import bp as solve_bp
app.register_blueprint(solve_bp)