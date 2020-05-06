from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import app
from app.models import User

@app.route('/')
@app.route('/index',)
@login_required
def index():
    return render_template('index.html', title="Home Page")


@app.route('/addquestion', methods=['GET', 'POST'])
def addQuestion():
    return render_template('addquestion.html')