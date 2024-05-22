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
    course_id = request.args.get("course_id")
    remove_id = request.args.get("remove_id")
    remove_all = request.args.get("remove_all")

    if remove_all:
        session[f"{current_user.id}"] = []

    if remove_id:
        obj_from_session = session.get(f"{current_user.id}", [])
        # Find the course object with the matching ID and remove it
        obj_from_session = [
            course_obj
            for course_obj in obj_from_session
            if course_obj["id"] != remove_id
        ]
        session[f"{current_user.id}"] = obj_from_session

    if course_id:
        course = Course.query.filter_by(id=course_id).first()

        if course:
            course_obj = {
                "id": course.id,
                "course_title": course.course_title.title(),
                "course_code": course.course_code,
                "course_unit": course.course_unit,
                "lecturer": f"{course.lecturer.last_name} {course.lecturer.first_name}",
            }

            obj_from_session = session.get(f"{current_user.id}", [])
            if course_obj not in obj_from_session:
                obj_from_session.append(course_obj)
                session[f"{current_user.id}"] = obj_from_session

    courses = Course.query.order_by(desc(Course.created_at)).all()

    courses_list = [
        {
            "id": course.id,
            "course_title": course.course_title.title(),
            "course_code": course.course_code,
            "course_unit": course.course_unit,
            "lecturer": f"{course.lecturer.last_name} {course.lecturer.first_name}",
        }
        for course in courses
    ]

    obj_from_session_list = session.get(f"{current_user.id}", [])
    total_items = len(obj_from_session_list)
    total_units = sum(
        [course_obj["course_unit"] for course_obj in obj_from_session_list]
    )
    return render_template(
        "student_templates/available_courses.html",
        registered_courses=True,
        alert=alert,
        bg_color=bg_color,
        courses=courses_list,
        selected_courses=obj_from_session_list,
        total_items=total_items,
        total_units=total_units,
    )
