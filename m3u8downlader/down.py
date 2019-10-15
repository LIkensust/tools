#!/usr/bin/env python
# coding=utf-8
import requests
#url = xxxxx.m3u8
url = "https://m3u8.130ju.com/wodedianying_water_m3u8/youmadianying/qiaotunmei/75_20190813000756207/75_20190813000756207.m3u8"
video_url = "https://m3u8.130ju.com/wodedianying_water_m3u8/youmadianying/qiaotunmei/75_20190813000756207/"
#获取m3u8文件的文本信息
all_content = requests.get(url=url, verify=False).text
#解析文本信息
file_line = all_content.split("\n")
#if file_line[0] != "#EXTM3U":
#    raise BaseException(u'非M3U8的链接')
#else:
unknow = True
for index, line in enumerate(file_line):
    try:
        if "#EXTINF" in line:
            print(line)
            unknow = False
            tmp = str(file_line[index + 1]).split('/')[-1]
            sl = len(tmp)
            tmp = tmp[:sl-1]
            pd_url = video_url + tmp
            print(pd_url)
            res = requests.get(pd_url, verify=False)
            #print(res)
            c_fule_name = str(file_line[index + 1]).split('/')[-1]
            sl = len(c_fule_name)
            c_fule_name = c_fule_name[:sl-1]
            print(c_fule_name)
            with open('.' + '/' + c_fule_name, 'ab') as f:
                f.write(res.content)
                f.flush()
            print('下载完成')
    except Exception as e:
        print(e)
