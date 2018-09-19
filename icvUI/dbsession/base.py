from icvUI.dbsession import *

# 获取相机功能列表
def query_application_data():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        application_list = []
        for k,v in application_config.items():
            if v == True:
                application_list.append(k)

        if not application_list:
            return []
        elif len(application_list) == 1:
            query_sql = "SELECT application_zh, application_en FROM application_map WHERE application_en = '{application_list[0]}';"
        else:
            query_sql = "SELECT application_zh, application_en FROM application_map WHERE application_en IN {tuple(application_list)};"
        cursor.execute(query_sql)
        data = cursor.fetchall()

        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 新增相机
def insert_new_camera(camera_id, camera_ip):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)      

        query_camera_id_sql = "SELECT camera_id,camera_ip FROM camera WHERE camera_id = '{camera_id}';"
        cursor.execute(query_camera_id_sql)
        data = cursor.fetchall()
        if data:
            return '你所填写的相机ID已存在，请更改后重新提交.'
    
        query_camera_ip_sql = "SELECT camera_id,camera_ip FROM camera WHERE camera_ip = '{camera_ip}';"
        cursor.execute(query_camera_ip_sql)
        data = cursor.fetchall()
        if data:
            return '你所填写的相机IP地址已存在，请更改后重新提交.'
        
        insert_sql = "INSERT INTO camera(camera_id,camera_ip) VALUES('{camera_id}','{camera_ip}');"
        cursor.execute(insert_sql)
        conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    finally:
        cursor.close()
        conn.close()

# 删除camera配置
def del_camera(camera_list):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)      

        if len(camera_list) == 1:
            delete_camera_sql = "DELETE FROM camera WHERE camera.camera_id = '{camera_list[0]}';"
            delete_ori_sql = "DELETE FROM intrusion_ori WHERE intrusion_ori.camera_id = '{camera_list[0]}';"
            delete_frame_sql = "DELETE FROM intrusion_first_frame WHERE intrusion_first_frame.camera_id = '{camera_list[0]}';"

        else:
            delete_camera_sql = "DELETE FROM camera WHERE camera_id IN {};".format(tuple(camera_list))
            delete_ori_sql = "DELETE FROM intrusion_ori WHERE camera_id IN {};".format(tuple(camera_list))
            delete_frame_sql = "DELETE FROM intrusion_first_frame WHERE camera_id IN {};".format(tuple(camera_list))
        
        cursor.execute(delete_camera_sql)
        conn.commit()

        cursor.execute(delete_ori_sql)
        conn.commit()

        cursor.execute(delete_frame_sql)
        conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    finally:
        cursor.close()
        conn.close()


# 查询camera表获取相机数据
def query_camera_data():
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)      

        # query_application_sql = "SELECT application_zh, application_en FROM application_map;"
        # cursor.execute(query_application_sql)
        # app_list = cursor.fetchall()
    
        # app_dict = {}
        # for i in app_list:
        #     app_dict[i['application_en']] = i['application_zh']

        query_sql = "SELECT camera_id, camera_ip, GROUP_CONCAT(application_map.application_zh) AS application, description FROM camera LEFT JOIN application_map ON FIND_IN_SET(application_map.application_en,camera.application) GROUP BY camera_id,camera_ip,description;"
        
        # query_sql = "SELECT camera_id,camera_ip,description,application FROM camera;"
        cursor.execute(query_sql)
        data = cursor.fetchall()

        # for i in data:
            # print(i)
            # app_zh_list = []
            # for j in i['application']:
            #     app_zh_list.append(app_dict[j])
            # i['application'] = ','.join(app_zh_list)
        # print(data)
        return data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

# 更新camera表相机数据
def update_camera_data(camera_id, camera_ip, application, description):
    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        # 更新camera表的功能和描述
        update_sql = "UPDATE camera SET camera_ip = '{}', application = '{}', description = '{}' WHERE camera_id = '{}';                  ".format(camera_ip, application, description, camera_id)
        cursor.execute(update_sql)
        conn.commit()

        # 删除intrusion_ori表中不属于越界功能的camera_id
        delete_intrusion_sql = "DELETE FROM intrusion_ori WHERE camera_id NOT IN (SELECT camera.camera_id FROM camera WHERE FIND_IN_SET('intrusion',application));"
        cursor.execute(delete_intrusion_sql)
        conn.commit()

        # 将camera表中属于越界功能的camera_id插入到intrusion_ori表中
        insert_intrusion_sql = "INSERT INTO intrusion_ori(camera_id) SELECT camera.camera_id FROM camera WHERE (FIND_IN_SET('intrusion',application) AND camera.camera_id NOT IN (SELECT intrusion_ori.camera_id FROM intrusion_ori));"
        cursor.execute(insert_intrusion_sql)
        conn.commit()

        # 删除panel_ori表中不属于面板功能的camera_id
        delete_panel_sql = "DELETE FROM panel_ori WHERE camera_id NOT IN (SELECT camera.camera_id FROM camera WHERE FIND_IN_SET('panel',application));"
        cursor.execute(delete_panel_sql)
        conn.commit()

        # 将camera表中属于面板功能的camera_id插入到panel_ori表中
        insert_panel_sql = "INSERT INTO panel_ori(camera_id) SELECT camera.camera_id FROM camera WHERE (FIND_IN_SET('panel',application) AND camera.camera_id NOT IN (SELECT panel_ori.camera_id FROM panel_ori));"
        cursor.execute(insert_panel_sql)
        conn.commit()

        return 'ok'
    except Exception as e:
        print(e)
        return '提交失败'
    finally:
        cursor.close()
        conn.close()




