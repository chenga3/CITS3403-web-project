from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import app
from app.models import User

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title="Home Page")
