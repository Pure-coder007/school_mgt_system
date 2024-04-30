from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required
from models import get_roles, Admin, get_admins, get_lecturers, create_course, get_courses, Course
from passlib.hash import pbkdf2_sha256 as hasher
from extensions import db
from utils import is_valid_email

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
    try:
        alert = session.pop('alert', None)
        bg_color = session.pop('bg_color', None)
        roles = get_roles()
        teams_list = get_admins()
        if request.method == 'POST':
            first_name = request.form.get('fname')
            last_name = request.form.get('lname')
            email = request.form.get('email')
            phone_number = request.form.get('phone')
            role = request.form.get('role')
            is_superadmin = request.form.get('is_superadmin')

            print("first_name: ", first_name, " last_name: ", last_name, " email: ", email,
                  " phone_number: ", phone_number, " role: ", role, " is_superadmin: ", is_superadmin)

            if not first_name or not last_name or not email or not phone_number or not role:
                alert = 'Please fill all the fields'
                bg_color = 'danger'
                return render_template('admin_templates/teams.html',
                                       alert=alert, bg_color=bg_color,
                                       teams=True, roles=roles,
                                       first_name=first_name, last_name=last_name,
                                       email=email, phone_number=phone_number,
                                       selected_role=role, is_superadmin=is_superadmin)

            if not is_valid_email(email):
                alert = 'Invalid email'
                bg_color = 'danger'
                return render_template('admin_templates/teams.html',
                                       alert=alert, bg_color=bg_color,
                                       teams=True, roles=roles, first_name=first_name, last_name=last_name, email=email,
                                       phone_number=phone_number, selected_role=role, is_superadmin=is_superadmin)

            email_exist = Admin.query.filter_by(email=email.lower()).first()
            if email_exist:
                alert = 'Email already exist'
                bg_color = 'danger'
                return render_template('admin_templates/teams.html',
                                       alert=alert, bg_color=bg_color,
                                       teams=True, roles=roles, first_name=first_name, last_name=last_name, email=email,
                                       phone_number=phone_number, selected_role=role, is_superadmin=is_superadmin)

            phone_exist = Admin.query.filter_by(phone_number=phone_number).first()
            if phone_exist:
                alert = 'Phone number already exist'
                bg_color = 'danger'
                return render_template('admin_templates/teams.html',
                                       alert=alert, bg_color=bg_color,
                                       teams=True, roles=roles, first_name=first_name, last_name=last_name, email=email,
                                       phone_number=phone_number, selected_role=role, is_superadmin=is_superadmin)

            admin_instance = Admin(
                first_name=first_name,
                last_name=last_name,
                email=email.lower(),
                phone_number=phone_number,
                role_id=role,
                is_superadmin=True if is_superadmin else False,
                password=hasher.hash("password")
            )

            db.session.add(admin_instance)
            db.session.commit()

            session['alert'] = f'{admin_instance.role.name.title()} added successfully'
            session['bg_color'] = 'success'

            return redirect(url_for('admin.teams'))

        return render_template('admin_templates/teams.html',
                               alert=alert, bg_color=bg_color, teams=True, roles=roles, teams_lists=teams_list)
    except Exception as e:
        print(e, "error@teams")
        db.session.rollback()
        session['alert'] = 'Network Error'
        session['bg_color'] = 'danger'
        return redirect(url_for('admin.teams'))


# courses
@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)
    lecturers = get_lecturers()
    all_courses = get_courses()
    if request.method == "POST":
        course_unit = request.form.get('course_unit')
        course_code = request.form.get('course_code')
        lecturer = request.form.get('lecturer')
        course_title = request.form.get('course_title')

        if not course_unit or not course_code or not course_title:
            alert = 'Please fill all the fields'
            bg_color = 'danger'
            return render_template('admin_templates/courses.html',
                                   alert=alert, bg_color=bg_color,
                                   courses=True, lecturers=lecturers, course_unit=course_unit,
                                   course_code=course_code, course_title=course_title, selected_lecturer=lecturer, all_courses=all_courses)

        print("course_unit: ", course_unit, " course_code: ", course_code,
              " course_title: ", course_title, " lecturer: ", lecturer)

        course_exist = Course.query.filter_by(course_code=course_code).first()
        if course_exist:
            alert = 'Course already exist'
            bg_color = 'danger'
            return render_template('admin_templates/courses.html',
                                   alert=alert, bg_color=bg_color,
                                   courses=True, lecturers=lecturers, course_unit=course_unit,
                                   course_code=course_code, course_title=course_title,
                                   selected_lecturer=lecturer, all_courses=all_courses)

        create_course(course_title, course_code, course_unit, lecturer)
        session['alert'] = 'Course added successfully'
        session['bg_color'] = 'success'
        return redirect(url_for('admin.courses'))
    return render_template('admin_templates/courses.html',
                           alert=alert, bg_color=bg_color,
                           courses=True, lecturers=lecturers, all_courses=all_courses)
