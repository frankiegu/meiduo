from icvUI.dbsession import *


# 获取越界、人脸、安全着装的历史记录日期
def query_months():
    try:
        months = {}
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        query_intrusion_months_sql = "SELECT DISTINCT DATE_FORMAT(time,'%Y-%m') AS time FROM intrusion_result;"
        cursor.execute(query_intrusion_months_sql)
        intrusion_months = cursor.fetchall()
        
        query_face_months_sql = "SELECT DISTINCT DATE_FORMAT(time,'%Y-%m') AS time FROM face_result;"
        cursor.execute(query_face_months_sql)
        face_months = cursor.fetchall()

        query_safedress_months_sql = "SELECT DISTINCT DATE_FORMAT(time,'%Y-%m') AS time FROM safedress_result;"
        cursor.execute(query_safedress_months_sql)
        safedress_months = cursor.fetchall()

        query_panel_months_sql = "SELECT DISTINCT DATE_FORMAT(time,'%Y-%m') AS time FROM panel_result;"
        cursor.execute(query_panel_months_sql)
        panel_months = cursor.fetchall()

        months = {
            "intrusion_months":intrusion_months,
            "face_months":face_months,
            "safedress_months":safedress_months,
            "panel_months":panel_months
        }
        return months
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 获取月份数据
def query_statistics_data(application, month):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        if application == 'intrusion':
            query_sql = "SELECT intrusion_result.camera_id, description, count(intrusion_result.camera_id) AS total FROM camera, intrusion_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND intrusion_result.camera_id = camera.camera_id GROUP BY intrusion_result.camera_id,description;"
            cursor.execute(query_sql)
            data = cursor.fetchall()

        if application == 'panel':
            query_sql = "SELECT panel_result.camera_id, description, count(panel_result.camera_id) AS total FROM camera, panel_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND panel_result.camera_id = camera.camera_id GROUP BY panel_result.camera_id,description;"
            cursor.execute(query_sql)
            data = cursor.fetchall()

        if application == 'face':
            
            query_camera_id_sql = "SELECT camera_id,description FROM camera WHERE FIND_IN_SET('face',application) ORDER BY camera_id;"
            cursor.execute(query_camera_id_sql)
            face_camera = cursor.fetchall()

            data = []
            for camera in face_camera:
                query_unknown_sql = "SELECT count(camera_id) AS total FROM face_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND face_result.person_name = '未知人员' AND camera_id = '{camera['camera_id']}' GROUP BY camera_id;"
                cursor.execute(query_unknown_sql)
                unknown_data = cursor.fetchone()

                query_known_sql = "SELECT count(camera_id) AS total FROM face_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND face_result.person_name != '未知人员' AND camera_id = '{camera['camera_id']}' GROUP BY camera_id;"
                cursor.execute(query_known_sql)
                known_data = cursor.fetchone()

                if not unknown_data:
                    unknown_data = {"total":0}
                if not known_data:
                    known_data = {"total":0}
                
                face_data = {
                    "camera_id":camera['camera_id'],
                    "description":camera['description'],
                    "alarm":[{
                        "alarm_type":"未知人员",
                        "total":unknown_data['total']
                    },{
                        "alarm_type":"已授权",
                        "total":known_data['total']
                    }]
                }

                data.append(face_data)  

        if application == 'safedress':
            query_camera_id_sql = "SELECT camera_id,description FROM camera WHERE FIND_IN_SET('safedress',application) ORDER BY camera_id;"
            cursor.execute(query_camera_id_sql)
            safedress_camera = cursor.fetchall()

            data = []
            for camera in safedress_camera:
                query_helmet_sql = "SELECT count(camera_id) AS total FROM safedress_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND FIND_IN_SET('helmet',alarm_type) AND camera_id = '{camera['camera_id']}' GROUP BY camera_id;"
                cursor.execute(query_helmet_sql)
                helmet_data = cursor.fetchone()

                query_clothes_sql = "SELECT count(camera_id) AS total FROM safedress_result WHERE DATE_FORMAT(time,'%Y-%m') = '{month}' AND FIND_IN_SET('work_clothes',alarm_type) AND camera_id = '{camera['camera_id']}' GROUP BY camera_id;"
                cursor.execute(query_clothes_sql)
                clothes_data = cursor.fetchone()

                if not helmet_data:
                    helmet_data = {"total":0}
                if not clothes_data:
                    clothes_data = {"total":0}
                
                safedress_data = {
                    "camera_id":camera['camera_id'],
                    "description":camera['description'],
                    "alarm":[{
                        "alarm_type":"helmet",
                        "total":helmet_data['total']
                    },{
                        "alarm_type":"work_clothes",
                        "total":clothes_data['total']
                    }]
                }
                data.append(safedress_data)

        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

