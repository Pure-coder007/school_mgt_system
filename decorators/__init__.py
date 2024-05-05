# import for decorators
from functools import wraps
from models import Admin
from flask import request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin_user = Admin.query.filter_by(id=current_user.id).first()
        # get previous endpoint
        # previous_endpoint = request.referrer
        # print(previous_endpoint, "previous endpoint")
        if not admin_user:
            session['alert'] = 'You cannot access this page'
            session['bg_color'] = 'danger'
            return redirect(url_for('student.student_dashboard'))
        return func(*args, **kwargs)
    return wrapper
