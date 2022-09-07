#!/usr/bin/python
# -*- coding:utf-8 -*-

import traceback




###基础配置×××××××××××××××××××××××××××××××××××××××××××××××××××××××
from Conf import *


###信息获取函数部分×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

from getfunction import *

###信息打印函数部分

from printfunction import *

#主程序×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

logging.info("epd7in5_V2 TL-Palace ")
epd = epd7in5_V2.EPD()



logging.info("Clear...")

epd.Clear()

#获取图片列表
photolist = getfunction.getFileList(photodir)
  
Minlong = -1
lastMinlong = -150
last_timestamp = 1660913901
while(1):
    try:
        ###每5秒处理一次******************************************************************************************************
        ##该模块下大多是信息的获取，可以本地获取的信息都可以5秒检测，需要联网获取的视情况每分钟获取或每小时获取
        
 
        ##获取时间
        timeget = getNowTime()
        nowMin = timeget[0]
        if not nowMin == lastMin:
            Minlong = Minlong + 1
            lastMin = nowMin
        nowHour = timeget[1]
        
        ##电量检测
        batteryget = getNowBattery()
        

        ###每小时处理一次******************************************************************************************************
        if not(nowHour == lastHour):
            
            ##
            logging.info("\n\n*******************************every hour************************************\n")
            lastHour = nowHour
            logging.info("now min {}, last min {}".format(nowMin,lastMin))
            logging.info("now hour {}, last hour {}".format(nowHour,lastHour))
            
            
              
        if (Minlong%1==0 and not Minlong == lastMinlong):
            ###每3分钟处理一次******************************************************************************************************
            if (Minlong%3==0):
                ##每3分钟进行一次网络内容的获取
                logging.info("\n\n*******************************every 3 minute**********************************\n")
                try:
                    logging.info(len(f_open_list))
                    for fp in f_open_list:
                        try:
                            fp.close()
                        except:
                            logging.info('photo not closed')
                            #pass

                    if len(f_open_list) >= 100:
                        f_open_list = []
                except:
                    pass
                #重置上一生命时间
                lastMinlong = Minlong
                logging.info("now Minlong {}".format(Minlong))
                
                ##创建画布
                Himage = Image.new('RGBA', (800, 480), white_bg)
                draw = ImageDraw.Draw(Himage)
                
                
                ##联网检查模块
                net = checkNet()
                printNet(Himage,draw,net)
                
                
                ##地址信息获取模块
                Locationget = getLocation(net)
                try:
                    cityname = Locationget[1]['city']
                except:
                    cityname = '北京'
                
                ##天气信息获取模块
                weatherget = getWeather(cityname,net)
                
                
                ##ToDolist获取模块
                todolist = getToDolist(net)


            ##每分钟进行一次屏幕刷新，以下是刷新的处理，该模块下大多是打印
            logging.info("\n\n*******************************every minute**********************************\n")

            #重置上一生命时间
            lastMinlong = Minlong
            logging.info("now Minlong {}".format(Minlong))

            #喝水检测
            water_remind_list = water_remind(last_timestamp,water_drink_time)

            ##创建画布
            Himage = Image.new('RGBA', (800, 480), white_bg)
            draw = ImageDraw.Draw(Himage)

            ##底栏432-480
            draw.rectangle((0, 430, 800, 480), outline = 0, fill = black_b)
            ##分割栏的线
            draw.line((183, 0, 183, 432), fill = black_b,width = 3)
            draw.line((183, 126, 800, 126), fill = black_b,width = 3)
            
            #wifi
            printNet(Himage,draw,net)
            
            
            ##天气信息打印模块
            printWeather(weatherget,Himage,draw)

            ##地址信息打印模块
            printLocation(Locationget,Himage,draw)
            
            ##时间信息打印模块
            printTime(timeget,lastMin,lastHour,draw)
            #重置上一时间
            lastMin = nowMin
            lastHour = nowHour

            ##课表打印模块
            drawclasslist(classconf,classlist,timeget,draw)
            
            ##电量信息打印模块
            printBattery(batteryget,percent=1,draw=draw)
                    
            ##ToDolist打印模块
            drawToDolist(todolist,timeget,draw)

            #多用途框绘制
            bg_pic = printpic(Himage,draw,net,timeget,photolist,water_remind_list, nwx=366,nwy=143)
            if water_remind_list[0] == True:
                water_remind_list[0] = False
                last_timestamp = int(time.time())
            
            #背景改变
            long_r = 800
            width_r = 480
            fp = open(os.path.join(picdir, 'white.png'),'rb')
            white_pic = Image.open(fp).convert('RGBA')
            f_open_list.append(fp)
            pic_resize = bg_pic.resize((long_r,width_r))#不改变长宽比的情况下改变图片大小为宽与框一样
            white_pic = white_pic.resize((long_r,width_r))#不改变长宽比的情况下改变图片大小为宽与框一样
            Himage1 = pic_resize.filter(MyGaussianBlur(radius=29)).convert('RGBA')

            Himage1 = Image.blend(Himage1, white_pic, 0.5)
            Himage1 = Himage1.convert('RGB')
            Himage1.paste(Himage, (0,0),Himage)
            Himage = Himage1

            
            
            ##显示
            epd.init()
            
            epd.Clear()
            
            time.sleep(1)
            
            epd.display(epd.getbuffer(Himage))
            
            time.sleep(1)
            
            epd.sleep()

            #转换图片
            if not (change_width==800 and change_height== 480):
                Himage = Himage.resize((change_width,change_height))#改变图片大小

            #保存横向图片
            name = "/home/wwwroot/default/output"+".jpg"
            Himage.save(name)
            name1 = "/home/wwwroot/default/bgpic"+".jpg"
            bg_pic.save(name1)
            logging.info("output picture saved!")
        
        #5秒处理一次基本事件
        time.sleep(5)
            
        
    except Exception as err:
        #如果没有正常打印课表信息
        logging.error("the while 1 goes wrong")
        logging.exception(err)
        time.sleep(5)
        

