from . import *
from icvUI import *
from flask import jsonify, request
import json
from icvUI.config import *

@script.route('/call_run',methods = ['GET','POST'])
def call_run():
    if request.method == 'POST':
        r = requests.post(run_url)
        print(r.text)
        return 'ok'
    return 'wrong'
        

@script.route('/call_intrusion_first',methods = ['GET','POST'])
def call_intrusion_first():
    if request.method == 'POST':
        r = requests.post(intrusion_first_frame_url)
        print(r.text)
        return 'ok'
    return 'wrong'


@script.route('/call_stop',methods = ['GET','POST'])
def call_stop():
    if request.method == 'POST':
        r = requests.post(stop_url)
        print(r.text)
        return 'ok'
    return 'wrong'

# @script.route('/call_face_input',methods = ['GET','POST'])
# def call_face_input():
#     if request.method == 'POST':
#         data = request.form
#         # file = request.files['file']
#         file = request.files['file']
#         print(file.read())
#         # r = requests.post(face_input_url,data = data,file = {"file":file})
#         # print(r.text)
#         # print(data,file)
#         return 'ok'
#     return 'wrong'