from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required

student = Blueprint('student', __name__)


# student dashboard
@student.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('student_templates/home.html',
                           student_dashboard=True, alert=alert, bg_color=bg_color)


@student.route('/registered_courses', methods=['GET'])
@login_required
def registered_courses():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('student_templates/reg_courses.html',
                           registered_courses=True, alert=alert, bg_color=bg_color)
