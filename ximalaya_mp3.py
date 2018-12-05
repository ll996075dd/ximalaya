__author__ = 'dzt'
__date__ = '2018/12/05 20:11'


# encoding: utf-8
import requests
import re
import sys
import random
from time import sleep
import json
import xlrd
import sys
import xlwt

sep = '\n'
sep1 = '*'*50 + '\n'
sep2 = '\n' + '*'*50 + '\n\n'

# url = 'https://www.ximalaya.com/youshengshu/4202564/'
Agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
         "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
         "Mozilla/5.0 "
         "(Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
         "Mozilla/5.0 "
         "(Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
         'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
         'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; '
         'MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
         'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); '
         '.NET CLR 2.0.50727; InfoPath.1)',
         'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; '
         'FunWebProducts)',
         'Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
         'Mozilla/5.0 (X11; U; Linux; pt-PT) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4'
         ]

# 获取源音频的 .m4a api
# API = 'https://www.ximalaya.com/revision/play/tracks?trackIds='

# .mp3 api地址
# API = 'http://mobile.ximalaya.com/mobile/playlist/album?albumId=%s&device=android&trackId=%s'
API = 'http://mobile.ximalaya.com/mobile/playlist/album?albumId=%s&device=android'

def randomAgent():
    headers = {'User-Agent': random.choice(Agent)}
    # print(headers)
    return headers


def XimaAPI(filename_api, outfilename):

    headers = randomAgent()
    fapi = open(filename_api, encoding='utf-8')
    fout = open(outfilename, 'w+', encoding='utf-8')

    for each in fapi:
        id = re.findall(r'\d+', str(each), re.S)
        # print('albumId:'+id[0])
        # print('trackId:'+id[1])
        # 只需要albumId
        # page_api = API % (id[0], id[1])
        page_api = API % (id[0])
        # print(page_api)
        res = requests.get(page_api, headers=headers).content
        res = json.loads(res)
        # print(res)
        data = res.get('data')
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('表1', cell_overwrite_ok=True)
        for i in data:
            playUrl64 = i.get('playUrl64')  # mp3 地址
            playUrl32 = i.get('playUrl32')
            albumImage = i.get('albumImage')  # 图片地址
            albumTitle = i.get('albumTitle')  # 专辑名字
            title = i.get('title')  # 音频名字
            # print(playUrl64)
            # print(albumImage)
            print(title + albumTitle)
            # print(type(title))
            # 获取index为行数
            a = data.index(i)
            fout.write("音频名字：%s 专辑名字：%s，图片地址：%s， mp3地址：%s" % (title, albumTitle, albumImage, playUrl64) + sep)
            # 行  列   数据
            sheet1.write(a, 0, title)
            sheet1.write(a, 1, "1")
            sheet1.write(a, 2, playUrl64)
            sheet1.write(a, 3, '')
            sheet1.write(a, 4, '1')
            sheet1.write(a, 5, '')
            sheet1.write(a, 6, albumTitle)
            sheet1.write(a, 7, '')
            sheet1.write(a, 8, '')
            sheet1.write(a, 9, '')
            sheet1.write(a, 10, '')
            sheet1.write(a, 11, '')
            sheet1.write(a, 12, albumImage)
            a += 1
            # break
        new_imei_file = '%s.xls' % id[0]
        f.save(new_imei_file)

    fapi.close()
    fout.close()


# 此方法可以手动添加 albumId 到 "ximalaya_ID.txt"中 直接进行爬取
if __name__ == '__main__':
    # url = sys.argv[1]
    XimaAPI("ximalaya_albumId.txt", "mp3_info.txt")
