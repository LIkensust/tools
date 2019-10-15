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

def downSrc(url,path) :
    all_content = requests.get(url,verify = False).text
    file_line = all_content.split("\n")
    if (len(file_line) == 0) | (file_line[0].find("#EXTM3U") == -1) :
        print("\t[error] can't get m3u8 file from url [" + url + "]")
        return False
    return True


def exitAndClean(clean_src,path,err) :
    if err :
        print("\t[error] download failed")
    if clean_src :
        if len(path) != 0 :
            os.rmdir(path)
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

    if ~downSrc(url,tmppath) :
        exitAndClean(clean_src,tmppath,True)
    #解析文件 1.内容校验 2.url判断

    #下载

    #合并
    

    #删除零时文件
    if clean_src :
        if(len(tmppath) != 0) :
            os.rmdir(tmppath)
            print("\t[info] clean m3u8 src files")
if __name__ == "__main__":
    if(len(sys.argv) < 2) :
        usage()
        sys.exit()
    main(sys.argv[2:],sys.argv[1])
