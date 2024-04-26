from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required

admin = Blueprint('admin', __name__)


# ADMIN-2024-660252

@admin.route('/admin', methods=['GET'])
def get_admin():
    return render_template('index.html')


# student_quarters
@admin.route('/student_quarters', methods=['GET', 'POST'])
@login_required
def student_quarters():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('admin_templates/student_quarters.html', alert=alert, bg_color=bg_color, student_quarters=True)


@admin.route('/admin_dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('admin_templates/home.html', alert=alert, bg_color=bg_color, admin_dashboard=True)


# teams
@admin.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('admin_templates/teams.html', alert=alert, bg_color=bg_color, teams=True)


# courses
@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    return render_template('admin_templates/courses.html', alert=alert, bg_color=bg_color, courses=True)
