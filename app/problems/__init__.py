from flask import Blueprint

bp = Blueprint('problems', __name__)

from app.problems import routes