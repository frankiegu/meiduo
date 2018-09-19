from icvUI.dbsession import *

# 获取属于面板功能的camera
def query_panel_camera():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT panel_ori.camera_id,description,ori_data FROM camera,panel_ori WHERE FIND_IN_SET('panel',application) AND panel_ori.camera_id = camera.camera_id ORDER BY panel_ori.camera_id;"

        cursor.execute(query_sql)
        data = cursor.fetchall()
        # print(data)
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

def query_panel_label():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT label_zh FROM panel_label;"
        cursor.execute(query_sql)
        data = cursor.fetchall()

        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取面板相机第一帧图片
def query_panel_first_frame(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        query_sql = "SELECT camera_id, frame_img FROM panel_first_frame WHERE camera_id = '{camera_id}';"
        cursor.execute(query_sql)

        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 插入面板数据
def update_panel_data(camera_id, ori_data):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
        update_sql = "UPDATE panel_ori SET ori_data = '{}' WHERE camera_id = '{}';".format(ori_data,camera_id)
        cursor.execute(update_sql)
        conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    finally:
        cursor.close()
        conn.close()

# 获取最新面板结果
def query_latest_panel(camera_id):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT description,panel_result.camera_id,status_type,alarm_data,panel_picture,DATE_FORMAT(time,'%Y-%m-%d %T') AS time,alarm_type FROM camera,panel_result WHERE panel_result.camera_id = '{camera_id}' AND camera.camera_id = panel_result.camera_id ORDER BY time DESC LIMIT 0,1;"

        cursor.execute(query_sql)
        data = cursor.fetchone()
        if not data:
            return None
        data['alarm_type'] = ",".join(list(data['alarm_type']))
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取全部面板结果
def query_panel_history(offset,limit,search):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)
                    
        if search == "正常":
            query_sql = "SELECT panel_result.camera_id,status_type,alarm_data,panel_picture,description,alarm_type,DATE_FORMAT(time,'%Y-%m-%d %T') AS time FROM camera,panel_result WHERE panel_result.camera_id = camera.camera_id AND panel_result.status_type = '正常' ORDER BY time DESC;"
        elif search == "异常":
            query_sql = "SELECT panel_result.camera_id,status_type,alarm_data,panel_picture,description,alarm_type,DATE_FORMAT(time,'%Y-%m-%d %T') AS time FROM camera,panel_result WHERE panel_result.camera_id = camera.camera_id AND panel_result.status_type = '异常' ORDER BY time DESC;"
        else:
            query_sql = "SELECT panel_result.camera_id,status_type,alarm_data,panel_picture,description,alarm_type,DATE_FORMAT(time,'%Y-%m-%d %T') AS time FROM camera,panel_result WHERE panel_result.camera_id = camera.camera_id ORDER BY time DESC;"

        cursor.execute(query_sql)
        data = cursor.fetchall()


        returndata = data[offset:offset+limit]
        for single in returndata:
            single['alarm_type'] = ",".join(list(single['alarm_type']))

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

# 日常拍照时间间隔
def update_panel_interval(interval):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT * FROM panel_daily_time;"
        cursor.execute(query_sql)
        data = cursor.fetchall()

        if len(data) == 0:
            insert_sql = "INSERT INTO panel_daily_time(time_interval) VALUES('{interval}');"
            cursor.execute(insert_sql)
            conn.commit()
        else:
            update_sql = "UPDATE panel_daily_time SET time_interval = '{interval}';"
            cursor.execute(update_sql)
            conn.commit()

        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    finally:
        cursor.close()
        conn.close()  

# 查询日常拍照时间间隔
def query_panel_interval():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_sql = "SELECT * FROM panel_daily_time;"
        cursor.execute(query_sql)
        data = cursor.fetchall()

        if len(data) == 0:
            data = ''
        else:
            time_hash = {
                "10":"10分钟",
                "30":"30分钟",
                "60":"1小时",
                "120":"2小时",
                "180":"3小时"
            }
            data[0]['time_interval'] = time_hash[data[0]['time_interval']]
            
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()  