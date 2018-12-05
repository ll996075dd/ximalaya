__author__ = 'dzt'
__date__ = '2018/12/05 21:33'

# encoding: utf-8
import requests
import re
import sys
import random
import json
from time import sleep

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
         "(Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
         ]

# 获取源音频的 .m4a api
API = 'https://www.ximalaya.com/revision/play/tracks?trackIds='

# .mp3 api地址
# API = 'http://mobile.ximalaya.com/mobile/playlist/album?albumId=%s&device=android&trackId=%s'
# API = 'http://mobile.ximalaya.com/mobile/playlist/album?albumId=%s&device=android'


def randomAgent():
    headers = {'User-Agent': random.choice(Agent)}
    # print(headers)
    return headers


def Xima(url):
    headers = randomAgent()
    r = requests.session().get(url, headers=headers)

    filename_id = "ximalaya_ID.txt"
    fout = open(filename_id, 'a+', encoding='utf-8')

    # <div class="text rC5T"><a title="《飞翔的秘密》[澳大利亚]伊莎·贾德" href="/youshengshu/4202564/134753995">《飞翔的秘密》[澳大利亚]伊莎·贾德</a></div>
    result = re.findall(r'<div class="text rC5T"><a title=".*?" href="(.*?)">(.*?)</a></div>', r.text, re.S)
    trackIds_list = []
    # print(result)
    for i in result:
        # 每个音频的地址
        second_url = i[0]
        # 每个音频的 title
        # print(second_url, i[1])

        res = re.findall(r'(?<=/)\d+$', second_url, re.S)
        # res = re.findall(r'\d+(?<![/])\d+', second_url, re.S)
        for x in res:
            print(x)

            fout.write("%s, %s" % (x, i[1]) + sep)
        # break

        # fout.write("%s,%s" % (second_url, i[1]) + sep)
    fout.close()


def get_more_page(url):
    headers = randomAgent()
    r = requests.session().get(url, headers=headers)
    pagenum = re.findall(r'<input type="number" placeholder="请输入页码" step="1" min="1" '
                         r'max="(\d+)" class="control-input tthf" value=""/>', r.text, re.S)
    pagenum = int(pagenum[0])
    if pagenum == []:
        pagenum = 1
    filename = "ximalaya_page.txt"
    fout = open(filename, 'w+', encoding='utf-8')
    # 循环获取每一页，这里暂时获取第一页
    for i in range(1, pagenum+1):
        # print(u'第' + str(i) + u'页')
        page_url = url + 'p{}/'.format(i)
        # print(page_url)
        # 爬取一页break
        fout.write("第%s页，%s" % (str(i), page_url) + sep)
        # break
    fout.close()
    return filename



def runXima(filename):
    f = open(filename, encoding='utf-8')
    for each in f:
        ip = re.findall(r'https.*/$', str(each), re.S)
        print(ip[0])
        Xima(ip[0])
        # sleep(1)


def XimaAPI(filename_api, outfilename):

    headers = randomAgent()
    fapi = open(filename_api, encoding='utf-8')
    fout = open(outfilename, 'w+', encoding='utf-8')
    for each in fapi:
        id = re.findall(r'\d+', str(each), re.S)
        print('trackId:'+id[0])
        page_api = API + id[0]
        # print(page_api)
        res = requests.get(page_api, headers=headers).content
        res = json.loads(res)
        # print(res)
        data = res.get('data')
        tracksForAudioPlay = data.get('tracksForAudioPlay')

        i = tracksForAudioPlay[0]

        playUrl64 = i.get('src')  # m4a 地址
        albumImage = i.get('trackCoverPath')  # 图片地址
        albumTitle = i.get('albumName')  # 专辑名字
        title = i.get('trackName')  # 音频名字
        # print(playUrl64)
        # print(playUrl32)
        # print(albumImage)
        print(title + albumTitle)

        fout.write("音频名字：%s 专辑名字：%s，图片地址：%s， m4a地址：%s" % (title, albumTitle, albumImage, playUrl64) + sep)


    fapi.close()
    fout.close()


if __name__ == '__main__':
    # url = sys.argv[1]
    filename = get_more_page('https://www.ximalaya.com/yinyue/4202564/')
    runXima(filename)
    XimaAPI('ximalaya_ID.txt', 'm4a_info.txt')
