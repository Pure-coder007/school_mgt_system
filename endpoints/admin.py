from flask import Blueprint, render_template, redirect, url_for

admin = Blueprint('admin', __name__)


# ADMIN-2024-660252

@admin.route('/admin', methods=['GET'])
def get_admin():
    return render_template('index.html')
