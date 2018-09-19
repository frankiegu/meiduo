from icvUI.dbsession import *

# 获取全部安全着装识别结果
def query_safedress_history(offset,limit):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT safedress_result.camera_id,picture,DATE_FORMAT(time,'%Y-%m-%d %T') AS time,description,GROUP_CONCAT(safedress_map.safedress_zh) AS alarm_type FROM camera,safedress_result LEFT JOIN safedress_map ON FIND_IN_SET(safedress_map.safedress_en,safedress_result.alarm_type) WHERE safedress_result.camera_id = camera.camera_id GROUP BY safedress_result.camera_id,picture,description,time ORDER BY time DESC;"
        
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

# 获取安全着装相机
def query_safedress_camera():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT camera_id, description FROM camera WHERE FIND_IN_SET('safedress',application);"
        cursor.execute(query_sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取最新安全着装结果
def query_latest_safedress(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT safedress_result.camera_id,picture,DATE_FORMAT(time,'%Y-%m-%d %T') AS time,description,GROUP_CONCAT(safedress_map.safedress_zh) AS alarm_type FROM camera,safedress_result LEFT JOIN safedress_map ON FIND_IN_SET(safedress_map.safedress_en,safedress_result.alarm_type) WHERE safedress_result.camera_id = '{}' GROUP BY safedress_result.camera_id,picture,description,time ORDER BY time DESC LIMIT 0,1 ;".format(camera_id)

        cursor.execute(query_sql)
        data = cursor.fetchone()
        # print(data)
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()
