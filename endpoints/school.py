from flask import Blueprint, render_template, redirect, url_for, session, request
from models import Admin
from flask_login import login_required, current_user, login_user, logout_user
from passlib.hash import pbkdf2_sha256 as hasher

school = Blueprint('school', __name__)


@school.route('/', methods=['GET'])
def landing_page():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('index.html', alert=alert, bg_color=bg_color)


@school.route('/login', methods=['GET', 'POST'])
def login():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)

    if request.method == 'POST':
        login_code = request.form.get('login_code')
        password = request.form.get('password')

        if not login_code or not password:
            alert = 'Please fill all the fields'
            bg_color = 'danger'
            return render_template('login.html', alert=alert, bg_color=bg_color, login_code=login_code,
                                   password=password)

        admin = Admin.query.filter_by(adm_id=login_code).first()

        if admin and hasher.verify(password, admin.password):
            session['alert'] = 'Login successful'
            session['bg_color'] = 'success'
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))
        alert = 'Invalid login code or password'
        bg_color = 'danger'
        return render_template('login.html', alert=alert, bg_color=bg_color, login_code=login_code, password=password)
    return render_template('login.html', alert=alert, bg_color=bg_color)


@school.route('/logout')
@login_required
def logout():
    logout_user()
    session['alert'] = 'Logout successful'
    session['bg_color'] = 'success'
    return redirect(url_for('school.landing_page'))
