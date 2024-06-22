from extensions import db
from datetime import datetime
from flask_login import UserMixin
from utils import hexid
from sqlalchemy import desc
from .course_registered import number_of_course_reg


# This is the model for the courses
class Course(db.Model, UserMixin):
    __tablename__ = "courses"
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    course_unit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    teacher_id = db.Column(db.String(50), db.ForeignKey("admin.id"))
    registered_courses = db.relationship(
        "CourseRegistered", backref="course", lazy=True, cascade="all, delete"
    )
    # the student_registered column, it is also a relationship with the CourseRegistered model
    # the viewonly=True makes it a read-only relationship
    # the overlaps="course,registered_courses" makes it a read-only relationship
    student_registered = db.relationship(
        "CourseRegistered",
        viewonly=True,
        overlaps="course,registered_courses",
        backref="student_",
    )

    def __repr__(self):
        return "<Course %r>" % self.course_title


def create_course(course_title, course_code, course_unit, teacher):
    course = Course(
        course_title=course_title,
        course_code=course_code,
        course_unit=course_unit,
        teacher_id=teacher,
    )
    db.session.add(course)
    db.session.commit()
    return course


# get courses
def get_courses(page, per_page):
    courses = Course.query.order_by(desc(Course.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    total_pages = courses.pages
    total_items = courses.total

    return (
        [
            {
                "id": course.id,
                "course_title": course.course_title,
                "course_code": course.course_code,
                "course_unit": course.course_unit,
                "created_at": course.created_at.strftime("%d-%b-%Y"),
                "student_reg": number_of_course_reg(course.id),
                "lecturer": f"{course.lecturer.last_name} {course.lecturer.first_name}",
            }
            for course in courses.items
        ],
        total_pages,
        total_items,
    )
