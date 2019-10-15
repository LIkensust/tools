#!/usr/bin/env python
# coding=utf-8
import os
import requests
import getopt
import sys

def usage() :
    print("============================================")
    print("||    Thanks for using m3u8downloader      ||")
    print("|| Usage: ~$ m3u8d yoururl [cmd1 [comd2]]  ||")
    print("|| cmd:----------------------------------  ||")
    print("|| -o: out_put_name    后接输出文件的文件名||")
    print("|| -c: clean_src_files 清除m3u8片段文件    ||")
    print("|| -h: help            打印帮助列表        ||")
    print("============================================")


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

    #解析文件 1.内容校验 2.url判断

    #下载

    #合并

if __name__ == "__main__":
    if(len(sys.argv) < 2) :
        usage()
        sys.exit()
    main(sys.argv[2:],sys.argv[1])
