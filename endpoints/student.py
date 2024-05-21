from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from extensions import db
from models import Student, Course
from decorators import student_required
from sqlalchemy import desc

student = Blueprint("student", __name__)


# student dashboard
@student.route("/student_dashboard", methods=["GET"])
@login_required
@student_required
def student_dashboard():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    return render_template(
        "student_templates/home.html",
        student_dashboard=True,
        alert=alert,
        bg_color=bg_color,
    )


@student.route("/registered_courses", methods=["GET"])
@login_required
@student_required
def registered_courses():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    return render_template(
        "student_templates/reg_courses.html",
        registered_courses=True,
        alert=alert,
        bg_color=bg_color,
    )


# edit profile
@student.route("/edit_profile", methods=["GET", "POST"])
@login_required
@student_required
def edit_profile():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not old_password or not new_password or not confirm_password:
            alert = "Please fill all the fields"
            bg_color = "danger"
            return render_template(
                "student_templates/edit_profile.html",
                student_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        if new_password != confirm_password:
            alert = "Passwords do not match"
            bg_color = "danger"
            return render_template(
                "student_templates/edit_profile.html",
                student_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        if not hasher.verify(old_password, current_user.password):
            alert = "Invalid old password"
            bg_color = "danger"
            return render_template(
                "student_templates/edit_profile.html",
                student_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        current_user.password = hasher.hash(new_password)
        current_user.changed_password = True
        db.session.commit()
        session["alert"] = "Password changed successfully"
        session["bg_color"] = "success"
        return redirect(url_for("student.student_dashboard"))

    return render_template(
        "student_templates/edit_profile.html",
        student_dashboard=True,
        alert=alert,
        bg_color=bg_color,
    )


# available courses
@student.route("/available_courses", methods=["GET"])
@login_required
@student_required
def available_courses():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)

    courses = Course.query.order_by(desc(Course.created_at)).all()

    courses_list = [
        {
            'id': course.id,
            'course_title': course.course_title.title(),
            'course_code': course.course_code,
            'course_unit': course.course_unit,
            'lecturer': f"{course.lecturer.last_name} {course.lecturer.first_name}"
        } for course in courses
    ]
    return render_template(
        "student_templates/available_courses.html",
        registered_courses=True,
        alert=alert,
        bg_color=bg_color,
        courses=courses_list
    )
