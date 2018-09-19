import os 
from icvUI.config import *
import subprocess

def call_intrusion_script():
    try:
        r = os.popen(intrusion_frame_script)
        print(r)
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'

def call_panel_script():
    try:
        r = os.popen(panel_frame_script)
        print(r)
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'

def call_main_script():
    try:
        r = subprocess.Popen(main_script,stdout=subprocess.PIPE,stdin = subprocess.PIPE, shell=True)
        print(r)
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
    
def call_face_script():
    try:
        r = os.popen(face_script)
        print(r)
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'


def call_stop_script():
    try:
        r = subprocess.Popen(stop_script,stdout=subprocess.PIPE,stdin = subprocess.PIPE, shell=True)
        print(r)
        return 'ok'
    except Exception as e:
        print(e)
        return 'wrong'
