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

if __name__ == "__main__":
    if(len(sys.argv) < 2) :
        usage()
        sys.exit()
    main(sys.argv[2:],sys.argv[1])
