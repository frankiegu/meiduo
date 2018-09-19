import requests
import os
import json
import re
from PIL import Image
from io import BytesIO
import mysql.connector as mc
from flask import (Flask, make_response, session,flash,
                    send_from_directory, request, url_for, 
                    render_template, jsonify, redirect)

from flask_login import (LoginManager, login_required,
                        logout_user, login_user, 
                        UserMixin, current_user)

from werkzeug.utils import secure_filename
from icvUI.config import *
from icvUI.dbsession import base as base_ds
from icvUI.dbsession import user as user_ds
from icvUI.dbsession import panel as panel_ds
from icvUI.dbsession import intrusion as intrusion_ds
from icvUI.dbsession import face as face_ds
from icvUI.dbsession import safedress as safedress_ds
from icvUI.dbsession import statistics as statistics_ds

# from icvUI.face_input_api import upload_face_picture #人脸录入API
from icvUI.call_script_handle.call import *
# import video_start

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = os.urandom(16)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.init_app(app)

from icvUI.api import api
app.register_blueprint(api)

from icvUI.ktp_single import single_app
app.register_blueprint(single_app)

from icvUI.call_script_handle import script
app.register_blueprint(script)

import icvUI.app
