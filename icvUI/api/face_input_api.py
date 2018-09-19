import os
import requests
from PIL import Image
from io import BytesIO
import mysql.connector as mc
from icvUI.config import fs_icv_db, img_save_path
from icvUI.call_script_handle.call import call_face_script


def upload_face_picture(person_name, person_id, face_train):

    try:
        conn = mc.connect(**fs_icv_db)
        cursor = conn.cursor(dictionary = True)

        # 检验前端输入的ID是否已经存在于数据库中
        query_sql = "SELECT person_id FROM face_input WHERE person_id = '{}';".format(person_id)
        cursor.execute(query_sql)
        data = cursor.fetchall()
        # print(data)
        if data:
           return {
                'data': None,
                'message': 'Bad Request! person_id already exists,please use other person_id.',
                'statusCode': 400,
                'success': False
            }
        
        response = requests.get(face_train)
        if response.status_code == 404:
            return {
                'data': None,
                'message': 'Bad Request! Please check your face_train resources.',
                'statusCode': 400,
                'success': False
            }
        image = Image.open(BytesIO(response.content))
        image.save(img_save_path + "{person_id}.jpg")

        insert_sql = "INSERT INTO face_input(person_name, person_id,face_train) VALUES('{}','{}','{}');".format(person_name, person_id, img_save_path + person_id + '.jpg')
        cursor.execute(insert_sql)
        conn.commit()
        call_face_script()
        return {
                'data': [],
                'message': 'success',
                'statusCode': 200,
                'success': True
            }
    except Exception as e:
        print(e)
        return {
                'data': None,
                'message': 'Bad Request!{}'.format(e),
                'statusCode': 400,
                'success': False
            }
    finally:
        cursor.close()
        conn.close()
