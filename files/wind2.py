# coding: utf-8 

import requests
import json
import datetime
import pytz

idToSinger={
    1530392: 'Sunnee',
    2141459: u'赖美云',
    2141458: u'傅菁',
    2141375: u'杨超越',
    2141439: u'紫宁',
    2141373: u'段奥娟',
    2141386: u'徐梦洁',
    2141217: u'吴宣仪',
    1527896: u'孟美岐',
    1512412: u'Yamy',
    2141486: u'李紫婷',
}


def getRankResponse():
    headers = {'Origin': 'https://y.qq.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    data = '{"comm":{"g_tk":5381,"uin":"1152921504914352727","format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"h5","needNewCode":1},"requestSingerCallList":{"method":"AlbumSingerRankList","param":{"actid":352},"module":"mall.AlbumCallSvr"},"requestUserInfo":{"method":"UsrCallInfo","param":{"actid":352},"module":"mall.AlbumCallSvr"}}'
    response = requests.post('https://u.y.qq.com/cgi-bin/musicu.fcg?_=1561938932dex.html?mid=0018oANt3Hd7ZE&_video=true&g_f=tuijianweeksalewell', headers=headers, data=data)
    return response.text


def getGroupSongResponse():    
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://y.qq.com/m/digitalbum/gold/index.html?mid=0018oANt3Hd7ZE&_video=true&g_f=tuijianweeksalewell',
        'Origin': 'https://y.qq.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('_', '1563562852970'),
    )
    data = '{"comm":{"g_tk":5381,"uin":0,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"h5","needNewCode":1},"requestCommonCallList":{"method":"AlbumCommonRankList","param":{"actid":352,"type":1},"module":"mall.AlbumCallSvr"},"requestUserInfo":{"method":"UsrCallInfo","param":{"actid":352},"module":"mall.AlbumCallSvr"}}'
    response = requests.post('https://u.y.qq.com/cgi-bin/musicu.fcg', headers=headers, params=params, data=data)
    ranklist = json.loads(response.text).get('requestCommonCallList').get('data').get('ranklist')
    counts = []
    for song in ranklist:
        counts.append(song.get('common_call_num'))
    return counts

def getTotalSale():
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://y.qq.com/m/digitalbum/gold/index.html?mid=0018oANt3Hd7ZE&_video=true&g_f=tuijianweeksalewell',
        'Origin': 'https://y.qq.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    params = (
        ('g_tk', '5381'),
        ('uin', '0'),
        ('format', 'json'),
        ('inCharset', 'utf-8'),
        ('outCharset', 'utf-8'),
        ('notice', '0'),
        ('platform', 'h5'),
        ('needNewCode', '1'),
        ('actid', '352'),
        ('albumid', '7031128'),
        ('albummid', '0018oANt3Hd7ZE'),
        ('queryprice', '1'),
        ('querylottery', '0'),
        ('ident_list', '0'),
        ('querycoloregg', '0'),
        ('querylbs', '0'),
        ('querylatest', '0'),
        ('actlist', ''),
        ('_', '1563566123295'),
    )
    response = requests.get('https://c.y.qq.com/shop/fcgi-bin/fcg_album_news', headers=headers, params=params)
    saleinfo = json.loads(response.text).get('data').get('saleinfo')
    assert (saleinfo.get('actid') == 352)
    return saleinfo.get('album_count')

def getRankList():
    saleToSinger = {}
    response = getRankResponse()
    print response
    jsonObject = json.loads(response)
    rankListJson = jsonObject.get('requestSingerCallList').get('data').get('ranklist')
    for singerJson in rankListJson:
        singerid = singerJson.get('singerid')
        saleToSinger.update({singerJson.get('singer_call_num'): idToSinger.get(singerid)})

    
    sum = 0    
    print
    south_africa = pytz.timezone('Asia/Shanghai')
    sa_time = datetime.datetime.now(south_africa)    
    print "      ", sa_time.strftime("%m/%d %H:%M")
    print "   销量  RMB差距(万)  歌手"
    pre=0
    for a,b in reversed(sorted(saleToSinger.items())):
        sum = sum+a
        if pre == 0:
            c=0
            pre=a
        else :
            c=(pre-a)*27
        print format(a,' 8d'),format(c/10000,' 10d'), ' ', b

    groupSongCounts = getGroupSongResponse()
    totalSale = getTotalSale();
    print " 风     ", groupSongCounts[0]
    print " 团歌2  ", groupSongCounts[1]
    print " 已售 ", totalSale
    under = totalSale-groupSongCounts[0]-groupSongCounts[1]-sum
    print " 未助燃", under, " 约", under*27/10000, "万"
    print
    print " 备注：RMB计算不到一万的直接去尾"
    print

getRankList()
