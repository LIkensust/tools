#!/usr/bin/env python
# coding=utf-8
import os
ts_path = "./"
path_list = os.listdir(ts_path)
path_list.sort()
input_name = ""
for files in path_list :
    if files.find('.ts') != -1 :
        input_name += ts_path+files + '|'
sl = len(input_name)
input_name = input_name[:sl-1]
print(input_name)
out_name = "video.mp4"
command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%    (input_name,out_name)
os.system(command)
    
