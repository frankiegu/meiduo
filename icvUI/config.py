# 功能配置
application_config = {
	"intrusion":True, #越界检测
	"face":True, #人脸识别
	"safedress":True,  #安全着装
	"panel":False, #面板识别
	"video":False #视频流
}

# 数据库配置
fs_icv_db = {
    'host':'192.168.1.241',
	'user':'root',
	'password':'!QAZ2wsx3edc',
	'port':3306,
	'database':'fs_icv_db',
	'charset':'utf8'
}

# 人脸图片存储路径配置,最后的 / 一定要加
# img_save_path = '/usr/local/icv/img/input_face/'
img_save_path = 'C:/Users/lenovo/Desktop/文件暂存地址/'

# 视频流存储路径
video_path = r'C:\Users\lenovo\Desktop\fs_icv\icvUI\static\video'

# 越界相机获取第一帧脚本
# intrusion_frame_script = "python3 /usr/local/icv/Eyes/get_first_img_intrusion.py"

# 面板相机获取第一帧脚本
panel_frame_script = "python3 /usr/local/icv/Eyes/get_first_img_panel.py"

# 人脸图片配置脚本
# face_script = "python3 /usr/local/icv/Eyes/put_face.py"

# 主程序脚本
# main_script = "cd /usr/local/icv/Eyes && ./icv.py restart"

# 停止程序脚本
# stop_script = "cd /usr/local/icv/Eyes && ./icv.py stop"

# 越界报警、人脸识别报警、安全着装报警api
face_api_url = 'http://localhost:5000/test'

intrusion_api_url = 'http://localhost:5000/test'

safedress_api_url = 'http://localhost:5000/test'


# 与opencv主机通信启动脚本URL
run_url = "http://192.168.1.79:5000/run"

intrusion_first_frame_url = "http://192.168.1.79:5000/first"

stop_url = "http://192.168.1.79:5000/stop"

face_input_url = "http://192.168.1.79:5000/face"
