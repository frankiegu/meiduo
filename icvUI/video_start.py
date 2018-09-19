import os
import subprocess
from config import *


script1 = r"ffmpeg -v verbose -i rtsp://admin:!QAZ2wsx3edc@192.168.1.168//Streaming/Channels/1 -c:v libx264 -c:a aac -ac 1 -strict -2 -crf 18 -profile:v baseline -s 640x360 -maxrate 400k -bufsize 1835k -pix_fmt yuv420p -flags -global_header -hls_time 10 -hls_list_size 6 -hls_wrap 10 -start_number 1 {}\play1.m3u8".format(video_path)

subprocess.Popen(script1,stdout=subprocess.PIPE,stdin = subprocess.PIPE, shell=True)

script2 = r"ffmpeg -v verbose -i rtsp://admin:!QAZ2wsx3edc@192.168.1.163//Streaming/Channels/1 -c:v libx264 -c:a aac -ac 1 -strict -2 -crf 18 -profile:v baseline -s 640x360 -maxrate 400k -bufsize 1835k -pix_fmt yuv420p -flags -global_header -hls_time 10 -hls_list_size 6 -hls_wrap 10 -start_number 1 {}\play2.m3u8".format(video_path)

subprocess.Popen(script2,stdout=subprocess.PIPE,stdin = subprocess.PIPE, shell=True)
