from flask import Blueprint, render_template, redirect, url_for, session, request

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
            session['alert'] = 'Please fill all the fields'
            session['bg_color'] = 'danger'
            return redirect(url_for('school.login'))

        if login_code == 'SCHOOL' and password == 'school':
            session['alert'] = 'Login successful'
            session['bg_color'] = 'success'
            return redirect(url_for('school.landing_page'))
        session['alert'] = 'Invalid login code or password'
        session['bg_color'] = 'danger'
        return redirect(url_for('school.login'))
    return render_template('login.html', alert=alert, bg_color=bg_color)
