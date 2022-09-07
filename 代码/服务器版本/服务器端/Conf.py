import sys                                     #系统
import logging                                 #日志
from PIL import Image,ImageDraw,ImageFont,ImageFilter      #绘图
import os                                      #文件
#from waveshare_epd import INA219               #电源模块电量获取
#from waveshare_epd import epd7in5_V2           #epd库
import time                                     #获取当前时间
import datetime                                 #建立日期对象
from borax.calendars.lunardate import LunarDate #用于转换农历和阳历
import timeout_decorator                        #定时器，超时报错
import socket                                   #提供访问网络服务
import requests                                 #网络申请
import urllib3                                  #参与网络协议
import math                                     #数学计算
import pypinyin                                 #转换中文和拼音
import random                                   #产生随机数


import userConf                                 #用户配置项

black_b = (0,0,0,255)
white = (255,255,255,255)
white_bg = (255,255,255,0)

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')                  #图片所在的位置
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')                  #库所在的位置
photodir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic/photos')         #随机展示图片所在位置
weathericondir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic/icons')    #天气图标所在位置
if os.path.exists(libdir):                                                                 #如果没有库文件夹添加库文件夹
    sys.path.append(libdir)


#页面大小设置
change_width = 800  #初始值800
change_height = 480 #初始值480

#右下多用途展框大小设置
multifunction_frame_width = 395   #初始值395
multifunction_frame_height = 276  #初始值276


#获取信息超时时间设置
timeout_s = 15


#日志输出部分
logging.basicConfig(
    filename ='/home/ubuntu/.local/TLPAlace_EPD/TLPAepd_Log.txt',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filemode = 'a',
    )

logging.info('###############################################################################\n\n\n')
logging.info('#                           a start of the log                                # \n\n\n')
logging.info('###############################################################################')


#电池部分
lowBatteryFlag = 0
#ina219 = INA219.INA219(addr=0x43)
chargingFlag = 0 #记录是否在充电，0为没有充电，1为在充电
powerConsumed = 0 #记录一共消耗多少电量


#地址部分
url1 = 'https://restapi.amap.com/v3/ip?parameters'
value1 = {
    'key' : userConf.GaoDekey,
    'ip': userConf.userip
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
    'key' : userConf.qweatherkey
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
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)


#时间部分初始化
lastMin = -150
lastHour = -150


#课表部分
classconf = userConf.classconf
classlist = userConf.classlist



#ToDolist部分
database_id=userConf.database_id
url_todo = "https://api.notion.com/v1/databases/" + database_id + "/query"

payload_todo = {"page_size": 100}
headers_todo = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Authorization": userConf.Authorization
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


#生日部分
birthday = userConf.birthday

#喝水时间设置
water_drink_time = userConf.water_drink_time


#pil高斯模糊的修改
class MyGaussianBlur(ImageFilter.Filter):
  name = "GaussianBlur"

  def __init__(self, radius=2, bounds=None):
    self.radius = radius
    self.bounds = bounds

  def filter(self, image):
    if self.bounds:
      clips = image.crop(self.bounds).gaussian_blur(self.radius)
      image.paste(clips, self.bounds)
      return image
    else:
      return image.gaussian_blur(self.radius)

#所有打开文件的列表
f_open_list = []