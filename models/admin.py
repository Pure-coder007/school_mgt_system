from extensions import db
from functools import wraps
from .students import code_generator
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from utils import hexid


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    name = db.Column(db.String(255))

    admin = db.relationship("Admin", backref="role", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"Role('{self.name}')"


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    # The id column is the primary key
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    # the first_name and last_name columns are not nullable
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # the adm_id column is unique and not nullable
    # the default value is a function that generates a unique code
    adm_id = db.Column(db.String(50), unique=True, nullable=False,
                       default=code_generator(f'ADMIN-{datetime.now().year}-')
                       )
    # the email column is unique and not nullable
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(50), nullable=True)
    role_id = db.Column(db.String(50), db.ForeignKey('role.id'), nullable=False)
    # the password column is not nullable
    password = db.Column(db.Text, nullable=False)

    # The __repr__ method is used to print the object
    def __repr__(self):
        return '<Admin %r>' % self.email


# This decorator is used to check if the logged-in user is an admin
# def admin_required(func):
#     # This wraps the function to be decorated
#     @wraps(func)
#     # This is the wrapper function
#     def wrapper(*args, **kwargs):
#         # Get the logged-in user
#         logged_user = get_jwt_identity()
#         # Check if the logged-in user is an admin
#         if not logged_user.startswith('ADMIN'):
#             # If not, return an error
#             abort(401, message="Admin access required")
#         return func(*args, **kwargs)
#     return wrapper


roles = ["lecturer", "admin", "ict", "dean", "hod"]


# propagate data inside the role table
def add_roles():
    for role in roles:
        new_role = Role(name=role)
        db.session.add(new_role)
    db.session.commit()
    return True


def get_roles():
    print("getting roles")
    roles = Role.query.all()
    if not roles:
        add_roles()
        roles = Role.query.all()
    return [{"id": role.id, "name": role.name} for role in roles]

# def create_admin():
#     admin = Admin(
#         first_name="Olawale",
#         last_name="Michael",
#         email="admin@localhost",
#         password=pbkdf2_sha256.hash("admin"),
#         is_superadmin=True,
#         role_id=Role.query.filter_by(name="admin").first().id
#     )
#     db.session.add(admin)
#     db.session.commit()
#     return True
