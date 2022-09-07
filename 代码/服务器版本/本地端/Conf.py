import sys
import logging
from PIL import Image,ImageDraw,ImageFont
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
photodir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic/photos')
weathericondir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic/icons')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import INA219
from waveshare_epd import epd7in5_V2
import time
import timeout_decorator
import math
import datetime
import socket
import requests
import urllib3
import pypinyin
import random


#日志输出部分
logging.basicConfig(
    #filename ='/home/pi/TLPAlace_EPD/TLPAepd_Log.txt',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filemode = 'a',
    #handlers = 'BaseRotatingHandler'
    )

logging.info('###############################################################################\n\n\n')
logging.info('#                           a start of the log                                # \n\n\n')
logging.info('###############################################################################')

#电池部分
lowBatteryFlag = 0
ina219 = INA219.INA219(addr=0x43)
chargingFlag = 0 #记录是否在充电，0为没有充电，1为在充电
powerConsumed = 0 #记录一共消耗多少电量


#地址部分
url1 = 'https://restapi.amap.com/v3/ip?parameters'
value1 = {
    'key' : '045668c0922d820f5a11761e8ad4946b',
    }
defaultLocation = {
    'status': '1',
    'info': 'OK',
    'infocode': '10000',
    'province': '四川省',
    'city': '成都市',
    'adcode': '510100',
    'rectangle': '103.9017713,30.53006918;104.2544496,30.79041003'
    }

#天气部分
url = 'https://devapi.qweather.com/v7/weather/3d'
value = {
    'location' : '101270107',
    'key' : 'c269ad4ed48a4a0387912cf6763087a5'
    #'lang' : 'zh'
    }
WitherGitFlag = 0 #天气获取flag
defaultWeather ={
    'code': '200',
    'updateTime': '2022-07-01T15:35+08:00',
    'fxLink': 'http://hfx.link/3tk1',
    'daily':
    [
        {
            #有用数据都变成0
            'fxDate': '0',
            'tempMax': '100',
            'tempMin': '0',
            'vis': '0',
            'uvIndex': '0',
            'humidity': '0',
            #其它数据无用，暂且不变
            'sunrise': '06:04',
            'sunset': '20:10',
            'moonrise': '07:35',
            'moonset': '22:05',
            'moonPhase': '峨眉月',
            'moonPhaseIcon': '801',
            'iconDay': '300',
            'textDay': '阵雨',
            'iconNight': '350',
            'textNight': '阵雨',
            'wind360Day': '0',
            'windDirDay': '北风',
            'windScaleDay': '1-2',
            'windSpeedDay': '3',
            'wind360Night': '0',
            'windDirNight': '北风',
            'windScaleNight': '1-2',
            'windSpeedNight': '3',
            'precip': '1.0',
            'pressure': '946',
            'cloud': '60'
            
            }
        ],
    'refer':
    {
        'sources':
        [
            'QWeather',
            'NMC',
            'ECMWF'
            ],
        'license': [
            'no commercial use'
            ]
        }
    }

#字体部分
font64 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 64)
font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
font44 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 44)
font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
font28 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 28)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)

#天气图标
weatherfont = ImageFont.truetype(os.path.join(picdir, 'qweather-icons.ttf'),40)

#时间部分初始化
lastMin = -150;
lastHour = -150;

#课表部分
classconf = {
    'startmonday':'2022-6-27',
    'weeks':'18'    
    }
classlist = {
    'class1':{
        'classname':'电子系统设计',
        'teachername':'none',
        'place':'立B217',
        'classweek':[1,2,5,9,10,11,12,13,14],#上课的周数，连续上18周就[range(1,19)]
        'classday':1,#周一到周日对应1到6 和 0
        'classnum':[4]#上午两节下午两节晚上一节，分别对应1到5
        },
    'class2':{
        'classname':'马原',
        'teachername':'龙小平',
        'place':'立B112',
        'classweek':[i for i in range(1,15+1)],
        'classday':2,
        'classnum':[2]
        },
    'class3':{
        'classname':'工程法律',
        'teachername':'J.L.E &J.P',
        'place':'立B217',
        'classweek':[1,3],
        'classday':2,
        'classnum':[4]
        },
    'class4':{
        'classname':'AI&ML',
        'teachername':'Bo',
        'place':'立B317',
        'classweek':[1,2,3,5,9,10,11,12,13,14],
        'classday':2,
        'classnum':[5]
        },
    'class5':{
        'classname':'信号与系统',
        'teachername':'AYNUL ISLAM',
        'place':'立B208',
        'classweek':[i for i in range(1,19)],
        'classday':3,
        'classnum':[3]
        },
    'class6':{
        'classname':'电子器件',
        'teachername':'Scott Roy',
        'place':'立B217',
        'classweek':[1,2,3,4,5,9,10,11,12,13,14],
        'classday':3,
        'classnum':[4]
        },
    'class7':{
        'classname':'工程法律',
        'teachername':'J.L.E &J.P',
        'place':'品A107',
        'classweek':[1,3,4],
        'classday':3,
        'classnum':[5]
        },
    'class8':{
        'classname':'马原',
        'teachername':'龙小平',
        'place':'立B112',
        'classweek':[i for i in range(1,15+1)],
        'classday':4,
        'classnum':[3]
        },
    'class9':{
        'classname':'电子器件',
        'teachername':'Scott Roy',
        'place':'立B217',
        'classweek':[3],
        'classday':4,
        'classnum':[4]
        },
    'class10':{
        'classname':'电子系统设计',
        'teachername':'Anthony',
        'place':'立B217',
        'classweek':[10,11,12],
        'classday':4,
        'classnum':[4]
        },
    'class11':{
        'classname':'AI&ML',
        'teachername':'Bo',
        'place':'立B317',
        'classweek':[2,3],
        'classday':4,
        'classnum':[5]
        },
    'class12':{
        'classname':'信号与系统',
        'teachername':'AI',
        'place':'立B208',
        'classweek':[i for i in range(1,19)],
        'classday':5,
        'classnum':[2]
        },
    'class3':{
        'classname':'工程法律',
        'teachername':'sad',
        'place':'立B217',
        'classweek':[1,2,5,9,11,12,13],
        'classday':5,
        'classnum':[4]
        }
    }


#ToDolist部分

database_id='2c0125f0c3e64cc0b8f4564c0ff9392e'
url_todo = "https://api.notion.com/v1/databases/" + database_id + "/query"

payload_todo = {"page_size": 100}
headers_todo = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Authorization": "Bearer secret_gH2eurPILoRxIBl8MsVdlzmwnZCdqgSuTnYvNWh7cCC"
}
defaultToDolist = [
    {
        'name': '出错了',
        'DDl': '2002-07-15',
        'checkbox': False,
        'star': 'star',
        'importance': '5'
        },
    {
        'name': '请重试',
        'DDl': '2002-08-25',
        'checkbox': False,
        'star': 'unstar',
        'importance': '5'
        },
    {
        'name': 'hahaha',
        'DDl': '2012-01-01',
        'checkbox': False,
        'star': 'unstar',
        'importance': '5'
        }
    
    ]

#图片部分
pic1 = Image.open(os.path.join(photodir, 'girl.png'))
pic2 = Image.open(os.path.join(photodir, 'HuLi.png'))
pic3 = Image.open(os.path.join(photodir, 'JiaRan.png'))
#pic4 = Image.open(os.path.join(photodir, 'lase.png'))
pic5 = Image.open(os.path.join(photodir, 'SeHuLi.png'))
pic6 = Image.open(os.path.join(photodir, 'yousa.bmp'))
pic7 = Image.open(os.path.join(photodir, 'miku.bmp'))
photolist = [
    pic1,pic2,pic3,pic5,pic6,pic7
    ]
