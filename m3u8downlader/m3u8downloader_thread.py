#!/usr/bin/env python
# coding=utf-8
import os
import requests
import getopt
import sys
import urllib3
import shutil
import threading
from tqdm import tqdm
import time

urllib3.disable_warnings()
file_list = []
name_list = []
file_index = 0
def usage() :
    print("============================================")
    print("||    Thanks for using m3u8downloader      ||")
    print("|| Usage: ~$ m3u8d yoururl [cmd1 [comd2]]  ||")
    print("|| cmd:----------------------------------  ||")
    print("|| -o: out_put_name    后接输出文件的文件名||")
    print("|| -c: clean_src_files 清除m3u8片段文件    ||")
    print("|| -n: no merge        不进行文件合并      ||")
    print("|| -l: limit           下载的片段数上限    ||")
    print("|| -t: thread num      同时下载的线程数    ||")
    print("|| -h: help            打印帮助列表        ||")
    print("============================================")

def getBeginUrl(url) :
    index = url.rfind("/")
    if index != -1 : 
        return url[:index+1]
    return ""

def downThread(path,bar,lock) :
    size = len(file_list)
    global file_index
    while True :
        lock.acquire()
        index = file_index
        file_index += 1
        #print index
        lock.release()
        if index >= size :
            break
        retry = 0 
        while retry < 3 :
            try :
                res = requests.get(file_list[index], verify=False, timeout = (10,120))
                break
            except requests.exceptions.RequestException :
                retry += 1
                print "retry [%s][%d]"% (file_list[index],retry)
        with open(path + '/' + name_list[index], 'ab') as f:
            f.write(res.content)
            f.flush()
        lock.acquire()
        bar.update(1)
        lock.release()
        #print(name_list[index])

def downSrc(url,path,limit_num, thread_num = 4) :
    if limit_num < 0:
        limit_num = 99999999;
    all_content = requests.get(url,verify = False).text
    file_line = all_content.split("\n")
    if (len(file_line) == 0) | (file_line[0].find("#EXTM3U") == -1) :
        print("\t[error] can't get m3u8 file from url [" + url + "]")
        return False
    begin_url = getBeginUrl(url) 
    total = len(file_line)
    #print(file_line)
    count = 0
    #file_list = []
    #name_list = []
    for index, line in enumerate(file_line) :
        if "#EXTINF" in line:
            tmp = str(file_line[index + 1]).split('/')[-1]
            tmpindex = tmp.rfind("ts")
            if (tmpindex == -1) :
                print("can't read m3u8 file")
                return False
            tmp = tmp[:tmpindex+2]
            c_fule_name = tmp
            if(tmp.find("http") != -1) :
                pd_url = tmp
            else :
                pd_url = begin_url + tmp;
            file_list.append(pd_url)
            name_list.append(c_fule_name)
            count = count + 1
            if count >= limit_num :
                break

    # 多线程下载
    # 每个线程均等分配任务
    file_num = len(file_list)
    pbar = tqdm(total = file_num)
    threadLock = threading.Lock()
    step = (int)(len(file_list) / thread_num)
    task = []
    #for i in range(0,thread_num - 1) :
    #    tmpurl = file_list[:step]
    #    tmpname = name_list[:step]
    #    file_list = file_list[step+1:]
    #    name_list = name_list[step+1:]
    #    t = threading.Thread(target = downThread, args = (tmpurl,tmpname,path,pbar,threadLock))
    #    task.append(t)
    #    t.start()

    #t = threading.Thread(target = downThread, args = (file_list,name_list,path,pbar,threadLock))
    #task.append(t)
    #t.start()
    for i in range(0, thread_num) :
        t= threading.Thread(target = downThread, args = (path,pbar,threadLock))
        task.append(t)
        t.start()
    #等待所有线程完成
    for t in task :
        t.join()

    return True

def merge(path,out_name) :
    ts_path = path + "/"
    path_list = os.listdir(ts_path)
    path_list.sort()
    input_name = ""
    for files in path_list :
        if files.find('.ts') != -1 :
            input_name += ts_path+files + '|'
    sl = len(input_name)
    input_name = input_name[:sl-1]
    command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%    (input_name,out_name)
    os.system(command)
 

def exitAndClean(clean_src,path,err) :
    if err :
        print("\t[error] download failed")
    if clean_src :
        if len(path) != 0 :
           # os.rmdir(path)
           shutil.rmtree(path)
    print("\t[info] down")
    sys.exit()

def main(argv,url) :
    out_file_name = "./m3u8d_output_video.mp4"
    clean_src = False
    no_merge = False
    limit_num = -1
    thread_num = 4
    try:
        opts, args = getopt.getopt(argv,"hcno:l:t:",["clean=","ofile="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-c","--clean") :
            clean_src = True
        elif opt in ("-o","ofile") :
            out_file_name = arg
        elif opt == "-l" :
            limit_num = int(arg)
        elif opt == "-n" :
            no_merge = True
        elif opt == "-t" :
            thread_num = int(arg)
        else : 
            usage()
            sys.exit()
    print "clean_src : [%r]"% (clean_src)
    print "url : [%s]"% (url)
    print "out_file_name : [%s]"% (out_file_name)
    print "limit_num : [%d]"% (limit_num)
    print "no merge : [%r]"% (no_merge)
    
    #创建零时文件夹
    sl = len(url)
    if sl >= 10 :
        tmppath = "./m3u8_tmp_path" + url[sl-10:]
    else :
        tmppath = "./m3u8_tmp_path" + url

    if os.path.exists(tmppath):
        print("\t[error] m3u8 tmp dir is already exist")
        if not no_merge :
            print("\t[info] try to merge")
    else :
        if os.mkdir(tmppath) :
            print("\t[error] can't create tmp dir")
            sys.exit()
        #下载m3u8文件
        
        if not downSrc(url,tmppath,limit_num, thread_num) :
            exitAndClean(clean_src,tmppath,True)

    #合并
    if not no_merge :
        merge(tmppath, out_file_name) 

    #删除零时文件
    exitAndClean(clean_src,tmppath,False)
     
    
if __name__ == "__main__":
    if(len(sys.argv) < 2) :
        usage()
        sys.exit()
    main(sys.argv[2:],sys.argv[1])
