from . import *
from icvUI import *
from flask import jsonify, request
import json
from .face_input_api import upload_face_picture

# @api.route('/test',methods=['GET','POST'])
# def test():
#     # data = request.json
#     # print(data)
#     return 'ok'

# 人脸识别api
@api.route('/icv/v1/face',methods=['GET','POST'])
def icv_v1_face():
    try:
        data = request.json
        person_picture = url_for('img_url_handle', filepath = data['person_picture'], _external=True)
        face_capture = url_for('img_url_handle', filepath = data['face_capture'], _external=True)
        data['person_picture'] = person_picture
        data['face_capture'] = face_capture

        r = requests.post(face_api_url,json = data)
        return 'ok'
    except Exception:
        return 'wrong'

# 越界检测api
@api.route('/icv/v1/intrusion',methods=['GET','POST'])
def icv_v1_intrusion():
    try:
        data = request.json
        intrusion_picture = url_for('img_url_handle', filepath = data['intrusion_picture'], _external=True)
        data['intrusion_picture'] = intrusion_picture

        r = requests.post(intrusion_api_url,json = data)
        return 'ok'
    except Exception:
        return 'wrong'
    
# 安全着装识别api
@api.route('/icv/v1/helmet',methods=['GET','POST'])
def icv_v1_helmet():
    try:
        data = request.json
        helmet_picture = url_for('img_url_handle', filepath = data['helmet_picture'], _external=True)
        data['helmet_picture'] = helmet_picture
        
        r = requests.post(safedress_api_url,json = data)
        return 'ok'
    except Exception:
        return 'wrong'

# 人脸录入api
@api.route('/icv/v1/face_input',methods=['GET','POST'])
def icv_v1_face_input():
    try:
        data = request.json
        # print(data)
        person_name = data['person_name'].strip()
        person_id = data['person_id'].strip()
        face_train = data['face_train'].strip()
        
        if '' in [person_id,person_name,face_train]:
            return jsonify({
                'data': None,
                'message': 'Bad Request! Please check your request body.',
                'statusCode': 400,
                'success': False
            })

        elif face_train[-3:] != 'jpg':
            return jsonify({
                'data': None,
                'message': 'Bad Request! Only accept pictures in JPG format.',
                'statusCode': 400,
                'success': False
            })

        elif not re.fullmatch(r'\d{8}',person_id):
            return jsonify({
                'data': None,
                'message': 'Bad Request! Only accept eight bits of person_id.',
                'statusCode': 400,
                'success': False
            })

        result = upload_face_picture(data['person_name'],data['person_id'],data['face_train'])
        return jsonify(result)
    except Exception as e:
        print(e)
        result = jsonify({
                "data":None,
                "message":"Bad Request!Please check your request body.",
                "statusCode":400,
                "success":False
            })
        return result 

