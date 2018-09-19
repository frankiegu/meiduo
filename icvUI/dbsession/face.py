from icvUI.dbsession import *

# 人脸设置页面图片验证
def verify_setting_face_picture(img_file, person_name, person_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        
        # 检验前端输入的ID是否已经存在于数据库中
        query_sql = "SELECT person_id FROM face_input WHERE person_id = '{}';".format(person_id)
        cursor.execute(query_sql)
        data = cursor.fetchall()
        if data:
           return '你所输入的ID已存在，请重新输入' 
        
        img_file.save(os.path.join(img_save_path, "{person_id}.jpg"))
        # insert_sql = "INSERT INTO face_input(person_name, person_id,face_train) VALUES('{}','{}','{}');".format(person_name,person_id,img_save_path + person_id + '.jpg')
        
        # cursor.execute(insert_sql)
        # conn.commit()
                
        return 'ok'
    except Exception as e:
        print(e)
        return '插入失败'
    finally:
        cursor.close()
        conn.close()

# 获取人脸识别相机
def query_face_camera():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT camera_id, description FROM camera WHERE FIND_IN_SET('face',application) ORDER BY camera_id;"
        cursor.execute(query_sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取最新人脸识别结果
def query_latest_face(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT face_result.camera_id, person_picture, face_capture, face_result.person_name, face_result.person_id, probability, DATE_FORMAT(face_result.time,'%Y-%m-%d %T') AS time, description, face_train FROM face_result, face_input, camera WHERE face_result.camera_id = '{}' AND face_result.person_id = face_input.person_id AND camera.camera_id = '{}' ORDER BY time desc limit 0,1;".format(camera_id,camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取全部人脸识别结果
def query_face_history(offset,limit):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT face_result.camera_id, description, DATE_FORMAT(face_result.time,'%Y-%m-%d %T') AS time ,face_result.person_name,face_result.person_id, probability, person_picture, face_capture, face_train FROM camera, face_result,face_input WHERE camera.camera_id = face_result.camera_id AND face_input.person_id = face_result.person_id ORDER BY time DESC;"

        cursor.execute(query_sql)
        data = cursor.fetchall()
        returndata = data[offset:offset+limit]
        result = {
            'total':len(data),
            'rows':returndata
        }
        return result

    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 插入人脸识别结果页上传的当前人脸图片验证
def verify_upload_face_capture(upload_person_name, upload_person_id, upload_face_train):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        # 检验前端输入的ID是否已经存在于数据库中
        query_sql = "SELECT person_id FROM face_input WHERE person_id = '{}';".format(upload_person_id)
        cursor.execute(query_sql)
        data = cursor.fetchall()
        # print(data)
        if data:
           return '你所输入的ID已存在，请重新输入'
        
        # response = requests.get(upload_face_train)
        # image = Image.open(BytesIO(response.content))
        # image.save(img_save_path + f"{upload_person_id}.jpg")
        # insert_sql = "INSERT INTO face_input(person_name, person_id, face_train) VALUES('{}','{}','{}');".format(upload_person_name, upload_person_id, img_save_path + upload_person_id + '.jpg')
        
        # cursor.execute(insert_sql)
        # conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return '录入失败,{}'.format(e)
    finally:
        cursor.close()
        conn.close()

def query_face_train():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT person_name,person_id,face_train FROM face_input;"
        cursor.execute(query_sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()
