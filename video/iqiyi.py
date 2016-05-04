# coding=utf8
"""
==============================================
This is a copy of the MIT license.
==============================================
Copyright (C) 2012, 2013, 2014 Mort Yao <mort.yao@gmail.com>
Copyright (C) 2012 Boyu Guo <iambus@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from uuid import uuid4
from random import random, randint
import json
from math import floor

from video.common import *
from video.definition import Definition
from video.exceptions import *
from utils.hash_util import md5_hex


'''
com.qiyi.player.core.model.def.DefinitonEnum
bid meaning for quality
0 none
1 standard
2 high
3 super
4 suprt-high
5 fullhd
10 4k
96 topspeed
'''

definition_mapping = {
    5: Definition.FHD,
    4: Definition.SHD,
    2: Definition.HD,
    1: Definition.SD,
}


def mix(tvid):
    enc = []
    enc.append('4a1caba4b4465345366f28da7c117d20')
    tm = str(randint(2000,4000))
    src = 'eknas'
    enc.append(str(tm))
    enc.append(tvid)
    sc = md5_hex("".join(enc))
    return tm, sc, src


def getVRSXORCode(arg1, arg2):
    loc3 = arg2 % 3
    if loc3 == 1:
        return arg1 ^ 121
    if loc3 == 2:
        return arg1 ^ 72
    return arg1 ^ 103


def getVrsEncodeCode(vlink):
    loc6 = 0
    loc2 = ''
    loc3 = vlink.split("-")
    loc4 = len(loc3)
    # loc5=loc4-1
    for i in range(loc4 - 1, -1, -1):
        loc6 = getVRSXORCode(int(loc3[loc4 - i - 1], 16), i)
        loc2 += chr(loc6)
    return loc2[::-1]


def getVMS(tvid, vid, uid):
    # tm -> the flash run time for md5 usage
    # um -> vip 1 normal 0
    # authkey -> for password protected video ,replace '' with your password
    # puid user.passportid may empty?
    # TODO: support password protected video
    tm, sc, src = mix(tvid)
    vmsreq = 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7' + \
                "&tvId=" + tvid + "&vid=" + vid + "&vinfo=1&tm=" + tm + \
                "&enc=" + sc + \
                "&qyid="+uid+"&tn="+str(random()) +"&um=0" +\
                "&authkey="+md5_hex(str(tm) + tvid)
    return json.loads(get_content(vmsreq))


def getDispathKey(rid):
    tp = ")(*&^flash@#$%a"  # magic from swf
    time = json.loads(get_content("http://data.video.qiyi.com/t?tn=" + str(random())))["t"]
    t = str(int(floor(int(time) / (10 * 60.0))))
    return md5_hex(t + tp + rid)


def get_real_addresses(url):
    """
    获取视频真实地址
    :param url:
    :return:
    """
    gen_uid = uuid4().hex
    html_content = get_content(url)

    tvid = match1(html_content, r'data-player-tvid="([^"]+)"')
    videoid = match1(html_content, r'data-player-videoid="([^"]+)"')
    assert tvid and videoid

    info = getVMS(tvid, videoid, gen_uid)
    assert info["code"] == "A000000"

    title = info["data"]["vi"]["vn"]

    # definition => real urls
    urls = {}
    if not info['data']['vp']['tkl']:
        raise VIPNotSupported(u'不支持VIP视频下载')

    for vs in info['data']['vp']['tkl'][0]['vs']:
        bid = int(vs['bid'])
        definition = definition_mapping.get(bid)
        if definition is None:
            continue
        video_links = vs['fs']
        if not vs["fs"][0]["l"].startswith("/"):
            tmp = getVrsEncodeCode(vs["fs"][0]["l"])
            if tmp.endswith('mp4'):
                video_links = vs["flvs"]
        urls[definition] = video_links

    for definition, video_links in urls.items():
        real_urls = []
        size = 0
        for i in video_links:
            vlink = i["l"]
            if not vlink.startswith("/"):
                vlink = getVrsEncodeCode(vlink)
            key = getDispathKey(vlink.split("/")[-1].split(".")[0])
            size += i["b"]
            base_url = info["data"]["vp"]["du"].split("/")
            base_url.insert(-1, key)
            url = "/".join(base_url) + vlink + '?su=' + gen_uid + '&qyid=' + uuid4().hex + \
                  '&client=&z=&bt=&ct=&tn=' + str(randint(10000, 20000))
            real_urls.append(json.loads(get_content(url))["l"])
        urls[definition] = real_urls

    return {
        'title': title,
        'urls': urls,
    }


if __name__ == "__main__":
    res = get_real_addresses('http://www.iqiyi.com/v_19rrolrmks.html')
    print res['title']
    print res['urls']
    for d, urls in res['urls'].items():
        print d
        for url in urls:
            print url
