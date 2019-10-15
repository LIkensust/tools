#!/usr/bin/env python
# coding=utf-8
import os
import requests
import getopt
import sys
import urllib3
urllib3.disable_warnings()

def usage() :
    print("============================================")
    print("||    Thanks for using m3u8downloader      ||")
    print("|| Usage: ~$ m3u8d yoururl [cmd1 [comd2]]  ||")
    print("|| cmd:----------------------------------  ||")
    print("|| -o: out_put_name    后接输出文件的文件名||")
    print("|| -c: clean_src_files 清除m3u8片段文件    ||")
    print("|| -h: help            打印帮助列表        ||")
    print("============================================")

def getBeginUrl(url) :
    index = url.rfind("/")
    if index != -1 : 
        return url[:index+1]
    return ""

def downSrc(url,path) :
    all_content = requests.get(url,verify = False).text
    file_line = all_content.split("\n")
    if (len(file_line) == 0) | (file_line[0].find("#EXTM3U") == -1) :
        print("\t[error] can't get m3u8 file from url [" + url + "]")
        return False
    begin_url = getBeginUrl(url) 
    total = len(file_line)
    print(file_line)
    for index, line in enumerate(file_line) :
        try :
            if "#EXTINF" in line:
                tmp = str(file_line[index + 1]).split('/')[-1]
                sl = len(tmp)
                tmp = tmp[:sl-1]
                if(tmp.find("http") != -1) :
                    pd_url = tmp
                else :
                    pd_url = begin_url + tmp;
                res = requests.get(pd_url, verify=False)
                c_fule_name = str(file_line[index + 1]).split('/')[-1]
                sl = len(c_fule_name)
                c_fule_name = c_fule_name[:sl-1]
                print c_fule_name
                with open(path + '/' + c_fule_name, 'ab') as f:
                    f.write(res.content)
                    f.flush()
        except Exception as e:
            print(e)
            return False
    
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
            os.rmdir(path)
    print("\t[info] down")
    sys.exit()

def main(argv,url) :
    out_file_name = "./m3u8d_output_video.mp4"
    clean_src = False
    try:
        opts, args = getopt.getopt(argv,"hco:",["clean=","ofile="])
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
        else : 
            usage()
            sys.exit()
    print(clean_src)
    print(url)
    print(out_file_name)

    #创建零时文件夹
    sl = len(url)
    if sl >= 10 :
        tmppath = "./m3u8_tmp_path" + url[sl-10:]
    else :
        tmppath = "./m3u8_tmp_path" + url

    if os.path.exists(tmppath):
        print("\t[error] m3u8 tmp dir is already exist")
        sys.exit()

    if os.mkdir(tmppath) :
        print("\t[error] can't create tmp dir")
        sys.exit()
    #下载m3u8文件

    if not downSrc(url,tmppath) :
        exitAndClean(clean_src,tmppath,True)

    #合并
    merge(tmppath, out_name) 

    #删除零时文件
    exitAndClean(clean_src,tmppath,False)
     
    
if __name__ == "__main__":
    if(len(sys.argv) < 2) :
        usage()
        sys.exit()
    main(sys.argv[2:],sys.argv[1])
