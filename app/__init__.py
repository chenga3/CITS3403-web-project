from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import threading
import subprocess
import redis
import rq

# initialse things
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

# function to start the redis worker
# def start_rq_worker(conn):
#     with rq.Connection(conn):
#         worker = rq.Worker(map(rq.Queue, ['yeetcode-judge']))
#         worker.work(logging_level='WARN')


# create a instance of the flask app
def create_app(config_class=Config):
    # app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initalise the stuff from above
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    #start worker
    
    app.redis = redis.Redis.from_url('redis://')

    # t = threading.Thread(target=start_rq_worker, args=(app.redis,))
    # t.start()

    #make redis queue
    app.task_queue = rq.Queue('yeetcode-judge', connection=app.redis)


    # Register Blueprints

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.problems import bp as problems_bp
    app.register_blueprint(problems_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models
