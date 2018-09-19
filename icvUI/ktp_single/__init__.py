from flask import Blueprint

single_app = Blueprint('single_app', __name__, template_folder='../templates/ktp/', static_folder='../static/ktp_js/')

from . import views
