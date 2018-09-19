from icvUI.dbsession import *

# 获取属于越界功能的camera
def query_intrusion_camera():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT intrusion_ori.camera_id,description,ori_data FROM camera,intrusion_ori WHERE FIND_IN_SET('intrusion',application) AND intrusion_ori.camera_id = camera.camera_id ORDER BY intrusion_ori.camera_id;"
        cursor.execute(query_sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取越界相机第一帧图片
def query_intrusion_first_frame(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT camera_id, frame_img FROM intrusion_first_frame WHERE camera_id = '{camera_id}';"
        cursor.execute(query_sql)

        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 插入越界数据
def update_intrusion_data(camera_id, ori_data):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        update_sql = "UPDATE intrusion_ori SET ori_data = '{}' WHERE camera_id = '{}';".format(ori_data,camera_id)
        cursor.execute(update_sql)
        conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    finally:
        cursor.close()
        conn.close()

# 获取最新越界结果
def query_latest_intrusion(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT description,intrusion_result.camera_id, intrusion_picture, DATE_FORMAT(time,'%Y-%m-%d %T') AS time FROM camera, intrusion_result WHERE intrusion_result.camera_id = '{}' AND camera.camera_id = intrusion_result.camera_id ORDER BY time desc limit 0,1;".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取全部越界结果
def query_intrusion_history(offset,limit):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT intrusion_result.camera_id, intrusion_picture, DATE_FORMAT(time,'%Y-%m-%d %T') AS time, description FROM intrusion_result,camera WHERE camera.camera_id = intrusion_result.camera_id ORDER BY time DESC;"

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
