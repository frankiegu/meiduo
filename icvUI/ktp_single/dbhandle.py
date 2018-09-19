import mysql.connector as mc
from icvUI.config import *

"""
越界检测
"""

# 查询相机是否配置好越界检测功能
def camera_is_intrusion(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT camera_id FROM camera WHERE camera_id = '{}' AND FIND_IN_SET('intrusion',application);".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

# 越界最新结果
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

# 获取单个相机越界历史结果给table展示
def query_intrusion_history(offset,limit,camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT intrusion_result.camera_id, intrusion_picture, DATE_FORMAT(time,'%Y-%m-%d %T') AS time, description FROM intrusion_result,camera WHERE camera.camera_id = intrusion_result.camera_id AND intrusion_result.camera_id = '{}' ORDER BY time DESC;".format(camera_id)

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

"""
安全着装
"""

# 查询相机是否配置好安全着装功能
def camera_is_safedress(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT camera_id FROM camera WHERE camera_id = '{}' AND FIND_IN_SET('safedress',application);".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

# 安全着装最新结果
def query_latest_safedress(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT safedress_result.camera_id,picture,DATE_FORMAT(time,'%Y-%m-%d %T') AS time,description,GROUP_CONCAT(safedress_map.safedress_zh) AS alarm_type FROM camera,safedress_result LEFT JOIN safedress_map ON FIND_IN_SET(safedress_map.safedress_en,safedress_result.alarm_type) WHERE safedress_result.camera_id = '{}' GROUP BY safedress_result.camera_id,picture,description,time ORDER BY time DESC LIMIT 0,1 ;".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取单个相机安全着装历史结果给table展示
def query_safedress_history(offset,limit,camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT safedress_result.camera_id,picture,DATE_FORMAT(time,'%Y-%m-%d %T') AS time,description,GROUP_CONCAT(safedress_map.safedress_zh) AS alarm_type FROM camera,safedress_result LEFT JOIN safedress_map ON FIND_IN_SET(safedress_map.safedress_en,safedress_result.alarm_type) WHERE safedress_result.camera_id = '{}' AND safedress_result.camera_id = camera.camera_id GROUP BY safedress_result.camera_id,picture,description,time ORDER BY time DESC;".format(camera_id)
        
        cursor.execute(query_sql)
        data = cursor.fetchall()

        returndata = data[offset:offset+limit]
        result = {
            'total':len(data),
            'rows':returndata
        }
        # print(result)
        return result
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

"""
人脸识别
"""

# 查询相机是否配置好人脸识别功能
def camera_is_face(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT camera_id FROM camera WHERE camera_id = '{}' AND FIND_IN_SET('face',application);".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

# 人脸识别最新结果
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
def query_face_history(offset,limit,camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT face_result.camera_id, description, DATE_FORMAT(face_result.time,'%Y-%m-%d %T') AS time ,face_result.person_name,face_result.person_id, probability, person_picture, face_capture, face_train FROM camera, face_result,face_input WHERE face_result.camera_id = '{}' AND camera.camera_id = face_result.camera_id AND face_input.person_id = face_result.person_id ORDER BY time DESC;".format(camera_id)

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
