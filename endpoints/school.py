from flask import Blueprint, render_template, redirect, url_for

school = Blueprint('school', __name__)


@school.route('/', methods=['GET'])
def landing_page():
    return render_template('index.html')


@school.route('/login', methods=['GET', 'POST'])
def login():
    alert = "This is login"
    bg_color = "success"
    return render_template('login.html', alert=alert, bg_color=bg_color)
