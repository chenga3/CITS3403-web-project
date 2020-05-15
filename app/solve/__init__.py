from flask import Blueprint

bp = Blueprint('solve', __name__)

from app.solve import routes