from . import *
from icvUI import *
from . import dbhandle
from flask import jsonify, request
import json


"""
越界URL
"""

# 越界UI
@single_app.route('/intrusion',methods =['GET','POST'])
def intrusion():
    try:
        if not request.args:
            return 'URL缺少参数'

        elif request.args['camera']:        
            camera_id = request.args['camera']
            isintrusion = dbhandle.camera_is_intrusion(camera_id)
            if isintrusion:
                return render_template('single_intrusion.html')
            else:
                return '此相机ID尚未配置越界检测功能'
    except:
        return '请求地址错误'  

# 越界最新数据
@single_app.route('/get_latest_single_intrusion',methods = ['GET','POST'])
def get_latest_single_intrusion():
    data = request.form
    result = dbhandle.query_latest_intrusion(data['camera_id'])

    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['intrusion_picture'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 越界UI table历史数据
@single_app.route('/get_single_intrusion_history', methods=['GET','POST'])
def get_single_intrusion_history():
    camera = request.args['camera']
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])
    result = dbhandle.query_intrusion_history(offset, limit, camera)

    if result:
        for data in result['rows']:
            img_url = url_for('img_url_handle', filepath = data['intrusion_picture'], _external=True)
            data.update({
                'imr_url':img_url
            })
        return jsonify(result)
    else:
        return jsonify({})

"""
安全着装URL
"""
# 安全着装识别UI
@single_app.route('/safedress',methods =['GET','POST'])
def safedress():
    try:
        if not request.args:
            return 'URL缺少参数'

        elif request.args['camera']:        
            camera_id = request.args['camera']
            issafedress = dbhandle.camera_is_safedress(camera_id)
            if issafedress:
                return render_template('single_safedress.html')
            else:
                return '此相机ID尚未配置安全着装识别功能'
    except:
        return '请求地址错误'  

# 安全着装最新数据
@single_app.route('/get_latest_single_safedress',methods = ['GET','POST'])
def get_latest_single_safedress():
    data = request.form
    result = dbhandle.query_latest_safedress(data['camera_id'])

    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['picture'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 安全着装UI table历史数据
@single_app.route('/get_single_safedress_history', methods=['GET','POST'])
def get_single_safedress_history():
    camera_id = request.args['camera']
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])
    result = dbhandle.query_safedress_history(offset, limit, camera_id)

    if result:
        for data in result['rows']:
            img_url = url_for('img_url_handle', filepath = data['picture'], _external=True)
            data.update({
                'imr_url':img_url
            })
        return jsonify(result)
    else:
        return jsonify({})


"""
人脸识别
"""
# 人脸识别UI
@single_app.route('/face',methods = ['GET','POST'])
def face():
    try:
        if not request.args:
            return 'URL缺少参数'

        elif request.args['camera']:        
            camera_id = request.args['camera']
            isface = dbhandle.camera_is_face(camera_id)
            if isface:
                return render_template('single_face.html')
            else:
                return '此相机ID尚未配置人脸识别功能'
    except:
        return '请求地址错误'  

# 人脸识别最新数据
@single_app.route('/get_latest_single_face',methods = ['GET','POST'])
def get_latest_single_face():
    data = request.form
    result = dbhandle.query_latest_face(data['camera_id'])

    if result:
        face_capture_url = url_for('img_url_handle', filepath = result['face_capture'], _external=True)
        face_train_url = url_for('img_url_handle', filepath = result['face_train'], _external=True)
        person_picture_url = url_for('img_url_handle', filepath = result['person_picture'], _external=True)

        result['face_capture'] = face_capture_url
        result['face_train'] = face_train_url
        result['person_picture'] = person_picture_url
        
        return jsonify(result)
    else:
        return ''

# 获取人脸识别结果给table展示
@app.route('/get_single_face_history',methods=['GET','POST'])
def get_single_face_history():
    camera_id = request.args['camera']
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    result = dbhandle.query_face_history(offset,limit,camera_id)

    if result:
        for data in result['rows']:
            face_capture_url = url_for('img_url_handle', filepath = data['face_capture'], _external=True)
            face_train_url = url_for('img_url_handle', filepath = data['face_train'], _external=True)
            person_picture_url = url_for('img_url_handle', filepath = data['person_picture'], _external=True)
            
            data['face_capture'] = face_capture_url
            data['face_train'] = face_train_url
            data['person_picture'] = person_picture_url
            
        return jsonify(result)
    else:
        return jsonify({})
