from icvUI import *

# url访问，send_from_directory下载图片
@app.route('/img_url_handle')
def img_url_handle():
    filepath = request.args['filepath']
    dirpath = filepath.rsplit('/', 1)[0]
    filename = filepath.rsplit('/', 1)[1]
    return send_from_directory(dirpath, filename)

class User(UserMixin):
    def __init__(self, group_id, user_name, user_code, role, pwd):
        self.group_id = group_id
        self.user_name = user_name
        self.user_code = user_code
        self.role = role
        self.pwd = pwd

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_code

# 从session中加载用户对象
@login_manager.user_loader
def load_user(usercode):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT * FROM account WHERE user_code = '{}';".format(usercode)
        cursor.execute(query_sql)
        userdata = cursor.fetchone()
        if userdata['user_code'] == usercode:
            user = User(userdata['group_id'], 
                    userdata['user_name'], 
                    userdata['user_code'], 
                    userdata['role'], 
                    userdata['pwd'])
            return user
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 验证用户名和密码
def verify_login(username,password):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        verify_sql = "SELECT * FROM account WHERE user_code = '{}' AND pwd = PASSWORD('{}');".format(username, password)
        
        cursor.execute(verify_sql)
        userdata = cursor.fetchone()

        if userdata is not None:
            user = User(userdata['group_id'], 
                        userdata['user_name'], 
                        userdata['user_code'], 
                        userdata['role'], 
                        userdata['pwd'])
            
            # 登录,传入用户对象,写到session中
            login_user(user)
            return True
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # 验证用户名密码
            if verify_login(username, password):
                return redirect(url_for('index'))		
            return redirect(url_for('login'))

        except Exception:
            return redirect(url_for('login'))

    return render_template('login.html')

# 注销
@app.route('/logout')
@login_required
#登录验证，是不是可以写一个装饰器来用
def logout():
    logout_user()
    return redirect(url_for('login'))

# 用户管理页面
@app.route('/manage')
@login_required
def usermanage():
    groups = user_ds.query_groups(current_user)
    return render_template('user_manage.html',current_user = current_user,groups = groups,application_config = application_config)

# 主页
@app.route('/')
@login_required
def index():
    return render_template('index.html', application_config = application_config)

# 越界检测结果UI
@app.route('/intrusion_all')
@login_required
def intrusion():
    result = intrusion_ds.query_intrusion_camera()
    return render_template('intrusion.html', intrusion_camera = result,application_config = application_config)

# 人脸识别结果UI
@app.route('/face_all')
@login_required
def face():
    result = face_ds.query_face_camera()
    return render_template('face.html',face_camera = result,application_config = application_config)

# 安全着装识别结果UI
@app.route('/safedress_all')
@login_required
def safedress():
    result = safedress_ds.query_safedress_camera()
    return render_template('safedress.html', safedress_camera = result,application_config = application_config)

# 统计报表UI
@app.route('/statistics')
@login_required
def statistics():
    result = statistics_ds.query_months()
    return render_template('statistics.html',months = result,application_config = application_config)

# 基本设置UI页面
@app.route('/base_setting')
# @login_required
def base_setting():
    data = base_ds.query_application_data()
    return render_template('base_setting.html',application = data,application_config = application_config)

# 人脸设置UI界面
@app.route('/face_setting',methods = ['GET','POST'])
@login_required
def face_setting():
    return render_template('face_setting.html',application_config = application_config)

# 越界设置UI页面
@app.route('/intrusion_setting')
@login_required
def intrusion_setting():
    data = intrusion_ds.query_intrusion_camera()
    return render_template('intrusion_setting.html',intrusion_camera = data,application_config = application_config)

# 面板设置页面
@app.route('/panel_setting',methods = ['GET','POST'])
@login_required
def panel_setting():
    data = panel_ds.query_panel_camera()
    labels = panel_ds.query_panel_label()
    time_interval = panel_ds.query_panel_interval()

    return render_template('panel_setting.html',panel_camera = data,labels = labels,application_config = application_config,interval_data = time_interval)
    
# 面板展示页面
@app.route('/panel',methods = ['GET','POST'])
@login_required
def panel():
    result = panel_ds.query_panel_camera()
    return render_template('panel.html',panel_camera = result,application_config = application_config)

# bootstrap—table取数据用
@app.route('/get_user_data')
@login_required
def get_user_data():
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])
    search_user = request.args['search']
    result = user_ds.query_user_data(current_user, offset, limit, search_user)
    # print(result)
    return jsonify(result)

# 添加用户	
@app.route('/useradd', methods=['GET','POST'])
@login_required
def useradd():
    username = request.form['username']
    usercode = request.form['usercode']
    password = request.form['password']
    role = request.form['role']
    userfrom = request.form['userfrom']

    result = user_ds.insert_user(username, usercode, password, role, userfrom)
    return result

# 修改用户
@app.route('/usermodify', methods=['GET','POST'])
@login_required
def usermodify():
    username = request.form['username']
    usercode = request.form['usercode']
    role = request.form['role']
    userfrom = request.form['userfrom']
    # print(username,usercode,role,userfrom)
    result = user_ds.update_user(username, usercode, role, userfrom)
    return result

# 删除用户
@app.route('/userdelete',methods=['GET','POST'])
@login_required
def userdelete():
    del_data = request.form['del_users']
    result = user_ds.delete_user(del_data)
    return result

# 修改密码
@app.route('/passwordmod',methods=['GET','POST'])
@login_required
def passwordmod():
    mod_pwd = request.form['password']
    mod_user = request.form['usercode']
    result = user_ds.update_password(mod_user,mod_pwd)
    return result

# 新增相机
@app.route('/add_new_camera',methods=['GET','POST'])
def add_new_camera():
    data = request.form
    result = base_ds.insert_new_camera(data['camera_id'],data['camera_ip'])
    return result

# 删除相机
@app.route('/del_camera',methods=['GET','POST'])
def del_camera():
    data = request.form
    result = base_ds.del_camera(json.loads(data['del_camera']))
    return result

# 基本设置table数据
@app.route('/get_camera', methods = ['GET','POST'])
def get_camera():
    result = base_ds.query_camera_data()
    return jsonify(result)

# 修改相机参数
@app.route('/update_camera',methods = ['GET','POST'])
def update_camera():
    data = request.form
    # print(data)
    camera_id = data['camera_id']
    camera_ip = data['camera_ip']
    application = data['application']
    description = data['description']

    result = base_ds.update_camera_data(camera_id, camera_ip, application, description)
    return result

# 获取越界相机第一帧图片
@app.route('/intrusion_first_frame',methods=['GET','POST'])
def intrusion_first_frame():
    data = request.form
    result = intrusion_ds.query_intrusion_first_frame(data['camera_id'])
    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['frame_img'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 更新越界参数
@app.route('/update_intrusion',methods = ['GET','POST'])
def update_intrusion():
    data = request.form
    result = intrusion_ds.update_intrusion_data(data['camera_id'],data['ori_data'])
    return result

# 获取越界ori内容给越界设置页面table展示
@app.route('/get_intrusion_ori',methods = ['GET','POST'])
def get_intrusion_ori():
    result = intrusion_ds.query_intrusion_camera()
    return jsonify(result)

# 获取面板参数给table展示
@app.route('/get_panel_ori',methods = ['GET','POST'])
def get_panel_ori():
    result = panel_ds.query_panel_camera()
    # print(result)
    return jsonify(result)

# 更新面板坐标标签参数
@app.route('/update_panel',methods=['GET','POST'])
def update_panel():
    data = request.form
    result = panel_ds.update_panel_data(data['camera_id'],data['ori_data'])
    return result

# 获取面板相机第一帧图片
@app.route('/panel_first_frame',methods=['GET','POST'])
def panel_first_frame():
    data = request.form
    result = panel_ds.query_panel_first_frame(data['camera_id'])
    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['frame_img'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 面板最新数据固定内容部分
def table_fixed(head,body):
    string = "<table class='table table-hover'><thead>{head}</thead><tbody>{body}</tbody></table>"
    return string

# 格式化处理面板数据
def table_stringify(result):
    ammeter_tbody = ''
    pressure_tbody = ''
    switch_tbody = ''

    ammeter_table = ''
    pressure_table = ''
    switch_table = ''

    for single in json.loads(result['alarm_data']):
        if single['label'] == '避雷器用检测表':
            ammeter_thead = "<tr><th>名称</th><th>{single['data']['type']}</th></tr>"
            tbody_tr_td = "<tr><td>{single['name']}</td><td>{single['data']['arg']}</td></tr>"
            ammeter_tbody += tbody_tr_td

        elif single['label'] == '气压计':
            pressure_thead = "<tr><th>名称</th><th>{single['data']['type']}</th></tr>"
            tbody_tr_td = "<tr><td>{single['name']}</td><td>{single['data']['arg']}</td></tr>"
            pressure_tbody += tbody_tr_td
        
        elif single['label'] == '开关':
            switch_thead = "<tr><th>名称</th><th>{single['data']['type']}</th></tr>"
            tbody_tr_td = "<tr><td>{single['name']}</td><td>{single['data']['arg']}</td></tr>"
            switch_tbody += tbody_tr_td

    if ammeter_tbody != '':
        ammeter_table = table_fixed(ammeter_thead,ammeter_tbody)
    if pressure_tbody != '':
        pressure_table = table_fixed(pressure_thead,pressure_tbody)
    if switch_tbody != '':
        switch_table = table_fixed(switch_thead,switch_tbody)

    return ammeter_table + pressure_table + switch_table

# 获取最新面板结果
@app.route('/get_latest_panel',methods=['GET','POST'])
def get_latest_panel():
    data = request.form
    result = panel_ds.query_latest_panel(data['camera_id'])

    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['panel_picture'], _external=True)
        result.update({
            'img_url':img_url
        })
        result.update({
            "table":table_stringify(result)
        })
        return jsonify(result)
    else:
        return ''

# 获取全部面板结果
@app.route('/get_panel_history',methods=['GET','POST'])
def get_panel_history():
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])
    search = request.args['search']

    result = panel_ds.query_panel_history(offset,limit,search)
    if result:
        for data in result['rows']:
            img_url = url_for('img_url_handle', filepath = data['panel_picture'], _external=True)
            data.update({
                'img_url':img_url
            })
            data.update({
            "table":table_stringify(data)
            })
        return jsonify(result)
    else:
        return jsonify({})

# 日常拍照时间间隔
@app.route('/update_interval',methods=['GET','POST'])
def update_interval():
    data = request.form
    result = panel_ds.update_panel_interval(data['interval'])
    return result

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 人脸录入插入数据
@app.route('/face_input',methods = ['GET','POST'])
def face_input():
    try:
        if request.method == 'POST':
            data = request.form
            img_file = request.files['file']
            person_name = data['person_name']
            person_id = data['person_id']

            if allowed_file(img_file.filename):
                # 验证上传的参数
                result = face_ds.verify_setting_face_picture(img_file, person_name, person_id)
                if result == 'ok': #数据验证成功
                    r = requests.post(face_input_url,data = data,files = {"file":open(img_save_path + person_id + '.jpg',"rb")})
                    if r.text == 'ok':
                        return 'ok'
                    return '上传失败!'
                else:
                    return result
            else:
                return '文件格式错误，请上传正确格式'
    except:
        return '上传失败'

# 人脸table
@app.route('/get_face',methods = ['GET','POST'])
def get_face():
    result = face_ds.query_face_train()
    if result:
        for data in result:
            img_url = url_for('img_url_handle', filepath = data['face_train'], _external=True)
            data.update({
                'img_url':img_url
            })
        return jsonify(result)
    else:
        return jsonify({})

# 获取最新越界结果
@app.route('/get_latest_intrusion',methods=['GET','POST'])
def get_latest_intrusion():
    data = request.form
    result = intrusion_ds.query_latest_intrusion(data['camera_id'])

    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['intrusion_picture'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 获取全部越界结果
@app.route('/get_intrusion_history',methods=['GET','POST'])
def get_intrusion_history():
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    result = intrusion_ds.query_intrusion_history(offset,limit)
    if result:
        for data in result['rows']:
            img_url = url_for('img_url_handle', filepath = data['intrusion_picture'], _external=True)
            data.update({
                'img_label':'<img class="history_img img-responsive"  src="{}" />'.format(img_url)
            })
        return jsonify(result)
    else:
        return jsonify({})

# 获取全部人脸识别结果
@app.route('/get_face_history',methods=['GET','POST'])
def get_face_history():
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    result = face_ds.query_face_history(offset,limit)
    
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

# 人脸识别页的上传当前人脸功能
@app.route('/upload_face_capture',methods=['GET','POST'])
def upload_face_capture():
    try:
        if request.method == 'POST':	
            data = request.form
            # 验证上传的数据
            result = face_ds.verify_upload_face_capture(data['person_name'],data['person_id'],data['face_train'])
            if result == 'ok':
                r = requests.post(face_input_url,data = data)
                if r.text == 'ok':
                    return 'ok'
                return '上传失败！'
            return result
    except:
        return '上传失败！'
        

# 获取最新的人脸识别结果
@app.route('/get_latest_face', methods=['GET','POST'])
def get_latest_face():
    data = request.form
    result = face_ds.query_latest_face(data['camera_id'])

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
        
# 获取全部安全着装结果
@app.route('/get_safedress_history',methods=['GET','POST'])
def get_safedress_history():
    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    result = safedress_ds.query_safedress_history(offset,limit)
    if result:
        for data in result['rows']:
            img_url = url_for('img_url_handle', filepath = data['picture'], _external=True)
            data.update({
                'img_label':'<img class="history_img img-responsive"  src="{}" />'.format(img_url)
            })
        return jsonify(result)
    else:
        return jsonify({})

# 获取最新安全着装结果
@app.route('/get_latest_safedress',methods=['GET','POST'])
def get_latest_safedress():
    data = request.form
    result = safedress_ds.query_latest_safedress(data['camera_id'])

    if result:
        # 转换路径成url访问形式
        img_url = url_for('img_url_handle', filepath = result['picture'], _external=True)
        result.update({
            'img_url':img_url
        })
        return jsonify(result)
    else:
        return ''

# 获取统计报表月份数据
@app.route('/get_statistics',methods=['GET','POST'])
def get_statistics():
    data = request.form
    result = statistics_ds.query_statistics_data(data['application'],data['month'])
    return jsonify(result)

# # 重启越界相机脚本获取第一帧图片
# @app.route('/restart_intrusion',methods=['GET','POST'])
# def restart_intrusion():
#     data = request.form
#     if data['status'] == 'restart':
#         result = call_intrusion_script()
#         return result

# # 重启越界相机脚本获取第一帧图片
# @app.route('/restart_panel',methods=['GET','POST'])
# def restart_panel():
#     data = request.form
#     if data['status'] == 'restart':
#         result = call_panel_script()
#         return result

# # 重启主脚本运行底层服务
# @app.route('/restart_main',methods=['GET','POST'])
# def restart_main():
#     data = request.form
#     if data['status'] == 'restart':
#         result = call_main_script()
#         return result

# # 重启人脸脚本
# @app.route('/restart_face',methods=['GET','POST'])
# def restart_face():
#     data = request.form
#     if data['status'] == 'restart':
#         result = call_face_script()
#         return result

# # 停止脚本
# @app.route('/stop_main',methods=['GET','POST'])
# def stop_main():
#     data = request.form
#     if data['status'] == 'stop':
#         result = call_stop_script()
#         return result

# @app.route('/video',methods=['GET','POST'])
# @login_required
# def video():
#     response = make_response(render_template('video.html',application_config = application_config))
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     return response


# @app.route('/video/<string:file_name>')
# def stream(file_name):
#     video_dir = video_path
#     return send_from_directory(directory=video_dir, filename=file_name)
  