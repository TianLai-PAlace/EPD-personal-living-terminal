from Conf import *
import getfunction

#画滑条
def drawSlidebar(x,y,width,draw,linewidth=2,r=10,num=50,startnum=0,stopnum=100,fontsize=20,color=black_b):
    #依次是：直线起始x，直线起始y，直线长度，绘图父元素，直线宽度，圆半径，使用值，起始值，停止值，使用字号，颜色（0黑white白）,RGB颜色（'#000000'黑，'#ffffff'白）
    #设置反色
    if color == white:
        recolor = 0
    if color == 0:
        recolor = white
    if color == '#000000':
        recolor = '#ffffff'
    if color == '#ffffff':
        recolor = '#000000'
    if color == (0,0,0,255):
        recolor = (255,255,255,255)
    if color == (255,255,255,255):
        recolor = (0,0,0,255)
    #确定是浮点型
    num = float(num)
    startnum = float(startnum)
    stopnum = float(stopnum)
    #防呆
    if startnum > stopnum:
        n = startnum
        startnum = stopnum
        stopnum = n
    if num < startnum:
        num = startnum
    if num > stopnum:
        num = stopnum
    #字体字号设置
    if fontsize == 20: fontn = font20
    elif fontsize == 12: fontn = font12
    elif fontsize == 16: fontn = font16
    elif fontsize == 24: fontn = font24
    elif fontsize ==  28: fontn = font28
    elif fontsize ==  32: fontn = font32
    elif fontsize ==  36: fontn = font36
    elif fontsize ==  40: fontn = font40
    elif fontsize ==  48: fontn = font48
    else: fontn = font20
    #绘图
    draw.line((x,y,x+width,y),width=linewidth,fill=color)#直线
    
    percent = float((num-startnum)/(stopnum-startnum))
    percentlong = int((width)*percent)#圆在直线的位置
    
    draw.ellipse((x+percentlong-r,y-r,x+percentlong+r,y+r),fill=color)#数字圆球
    
    draw.text((x-len(str(int(startnum)))*10-10,y-12),str(int(startnum)), font = font20, fill=color)#开始数字
    
    draw.text((x+width+10,y-12),str(int(stopnum)), font = font20, fill=color)#结束数字
    
    drawnum = str(int(num))
    xx = x+percentlong+r-int(fontsize/2)*(len(list(drawnum))+1)
    yy = y-int(fontsize/2)
    
    draw.text((xx, yy), drawnum, font = fontn, fill = recolor)#实际数字
    
    


#画圆角矩形
def drawRoundedRectangle(x,y,width,height,r,color,draw):
    ##依次是： 起始x，起始y，矩形宽，矩形高，矩形圆角半径，绘图
    draw.rectangle((x+r, y, x+width-r, y+height),  fill = color)
    draw.rectangle((x, y+r, x+width, y+height-r),  fill = color)
    draw.ellipse((x,y,x+2*r,y+2*r),fill = color)#左上
    draw.ellipse((x+width-2*r,y,x+width,y+2*r),fill = color)#右上
    draw.ellipse((x,y+height-2*r,x+2*r,y+height),fill = color)#左下
    draw.ellipse((x+width-2*r,y+height-2*r,x+width,y+height),fill = color)#右下
    

#自动换行的文本
def drawtextautoline(nwx:int,
                     nwy:int,
                     str_in:str,
                     fontsize,
                     fontsize_in_num:int,
                     line_length_px:int,
                     color,
                     draw):
    try:
        #基础参数初始化
        list_str = list(str_in)#字符串转成列表
        line_long = 0#单行长度计数
        rows = 0#行数
        #防呆
        if line_length_px < fontsize_in_num:
            line_length_px = fontsize_in_num + 1
        
        
        for item in list_str:
            
            
            #打印这个字符
            now_x = nwx+line_long
            now_y = nwy+rows*fontsize_in_num
            draw.text((now_x,now_y),item,font = fontsize,fill = color)
            
            #判断是否中文
            if '\u4e00' <= item <= '\u9fff':#如果是中文
                line_long = line_long + fontsize_in_num
            elif item == "w":
                line_long = line_long + int(fontsize_in_num/1.8)
            elif item == "m":
                line_long = line_long + int(fontsize_in_num)
            else:
                line_long = line_long + int(fontsize_in_num/2)
            #判断是否换行
            if line_long >= line_length_px:
                line_long = 0
                rows = rows + 1
            
    except Exception as err:
        logging.info("not printed (from function drawtextautoline)")
        logging.exception(err)

#打印联网信息
def printNet(Himage,draw,net,nwx=15,nwy=432):
    #draw.arc((50,440,80,470), start = 225, end = 315, fill = white)
    global f_open_list
    logging.info("wifi drawed")
    wifi = Image.open(os.path.join(picdir, 'wifi.png'))
    f_open_list.append(wifi)
    Himage.paste(wifi, (nwx,nwy),wifi)
    if not net:
        draw.line((nwx,nwy,nwx+48,nwy+48),fill=white,width=3)
        

#打印图片（之后会联网获取）
def printpic(Himage, draw, net, timeget, photolist, water_remind, nwx=366,nwy=144):
    birthdayflag = False
    global f_open_list
    random_num = random.random()
    water_remind_flag = water_remind[0]
    now_timestamp = water_remind[1]

    framelong = multifunction_frame_width
    framewidth = multifunction_frame_height

    ##右下框绘图
    drawRoundedRectangle(nwx-3,nwy-3,framelong+6,framewidth+6,1,black_b,draw)
    drawRoundedRectangle(nwx+3,nwy+3,framelong-6,framewidth-6,1,white,draw)

    
    try:

        for person in birthday:
            if person["calendar"] == "Chinese Calendar":
                if timeget[6] == person["month"] and timeget[7] == person["date"]:
                    birthdayflag = True
                    print(birthdayflag)
            if person["calendar"] == "Solar Calendar":
                if timeget[8] == person["month"] and timeget[9] == person["date"]:
                    birthdayflag = True
                    print(birthdayflag)

        

        #随机挑选一张图片展示
        pic = random.choice(photolist)
        logging.info("the name of picture "+ pic.filename)

        ##1:联网检查报警
        if not net:
            draw.text((nwx+20,nwy+20),'ERROR-设备未联网',fill = black_b,font = font28)
            draw.text((nwx+20,nwy+60),'请连接设备热点为设备配网',fill = black_b,font = font28)
            draw.text((nwx+20,nwy+120),'热点名： TLPA-AP-xxx',fill = black_b,font = font28)
            draw.text((nwx+20,nwy+160),'设备将在5分钟内联网回复',fill = black_b,font = font28)
        
        ##2：生日检测提醒
        elif birthdayflag and random_num<0.4:
            #生日蛋糕图片

            birthday_photo = Image.open(os.path.join(picdir, 'birthday_white.bmp'))
            f_open_list.append(birthday_photo)
            birthday_photo = birthday_photo.resize((int(framelong*0.3),int(framelong*0.3)))
            long,width = birthday_photo.size
            Himage.paste(birthday_photo, (int(nwx+framelong/2-long/2),nwy+int(framewidth*0.1)))
            
            #文字提醒
            person_name = ""
            for person in birthday:
                if person["calendar"] == "Chinese Calendar":
                    if int(timeget[6]) == person["month"] and int(timeget[7]) == person["date"]:
                        person_name = person_name + (person["name"]) + "、"
                if person["calendar"] == "Solar Calendar":
                    if int(timeget[8]) == person["month"] and int(timeget[9]) == person["date"]:
                        person_name = person_name + (person["name"]) + "、"
            person_name_len = len(person_name)
            
            str_in = person_name[:-1] + "今天要过生日啦，快去送上祝福吧~"
            drawtextautoline(nwx+40,nwy+width+int(framewidth*0.1),str_in,font22,22,framelong-40*2,black_b,draw)
            logging.info(str_in)


        ##3: 喝水提醒
        elif water_remind_flag:
            #喝水图片

            drink_water_photo = Image.open(os.path.join(picdir, 'drinkwater.png'))
            f_open_list.append(drink_water_photo)
            drink_water_photo = drink_water_photo.resize((int(framelong*0.3),int(framelong*0.3)))
            long,width = drink_water_photo.size
            Himage.paste(drink_water_photo, (int(nwx+framelong/2-long/2),nwy+int(framewidth*0.1)), drink_water_photo)
            #文字提醒
            str_in = "喝水时间到啦，快来补充一下水分吧"
            drawtextautoline(nwx+40,nwy+width+int(framewidth*0.1),str_in,font22,22,framelong-40*2,black_b,draw)
            

        ##4:随机图片展示
        else:
            logging.info("picture drawed")
            

            #获取图片长宽并计算长宽比
            long,width = pic.size
            lwrato = float(long/width)#图片长宽比
            lwrato_ori = float(framelong/framewidth)#展示框长宽比
            
            #计算图片长宽比和展示框长宽比的差
            value_difference = lwrato - lwrato_ori
            
            #计算差的绝对值
            if value_difference < 0:
                absolute_value_difference = -value_difference
            else:
                absolute_value_difference = value_difference
            
            #如果二者长宽比相差不大，就直接resize
            if absolute_value_difference<=0.3:
                pic_resize = pic.resize((framelong,framewidth))
                Himage.paste(pic_resize, (nwx,nwy))
            
            #如果二者长宽比相差较大且原图像更倾向于竖向
            elif absolute_value_difference>0.3 and value_difference<-0.3:
                #背景
                long_r = framelong
                width_r = int(framelong/lwrato)
                pic_resize = pic.resize((long_r,width_r))#不改变长宽比的情况下改变图片大小为宽与框一样
                pic_crop = pic_resize.crop((0,int(width_r/2-framewidth/2),framelong,int(width_r/2+framewidth/2)))#截取长图中间部分
                pic_filter = pic_crop.filter(MyGaussianBlur(radius=29))
                Himage.paste(pic_filter, (nwx,nwy))

                #图片
                long_r = int(framewidth*lwrato)
                width_r = framewidth
                pic_resize = pic.resize((long_r,width_r))#不改变长宽比的情况下改变图片大小为高与框一样
                Himage.paste(pic_resize, (int(nwx+framelong/2-long_r/2),nwy))#图片中心放置

                
            #如果二者长宽比相差较大且原图像更长,横向长图
            elif absolute_value_difference>0.3 and value_difference>0.3:
                long_r = framelong
                width_r = framewidth
                pic_resize1 = pic.resize((int(framewidth*lwrato),framewidth))#不改变长宽比的情况下将图片高度适配相框高度
                pic_crop = pic_resize1.crop((int((framewidth*lwrato)/2-framelong/2),0,int((framewidth*lwrato)/2+framelong/2),framewidth))#截取长图中间部分
                Himage.paste(pic_crop, (nwx,nwy))
            
            #如果今日有人过生日，会有一个生日蛋糕的图标
            if random_num>=0.4 and birthdayflag:
                birthday_photo = Image.open(os.path.join(picdir, 'birthday.bmp'))
                birthday_photo_size = int(framelong*0.1)
                birthday_photo = birthday_photo.resize((birthday_photo_size,birthday_photo_size))
                Himage.paste(birthday_photo, (nwx+framelong-birthday_photo_size,nwy+framewidth-birthday_photo_size))
            
        #返回
        return pic

            
    except Exception as err:
        #draw.text((nwx, nwy), "出错了", font = font48, fill = black_b)
        drawtextautoline(nwx,
                     nwy,
                     err,
                     font24,
                     24,
                     framelong,
                     0,draw)
        logging.error("the photo  printed goes wrong")
        logging.exception(err)
        #返回
        Himage1 = Image.open(os.path.join(photodir, 'IMG_0995(20211103-130004).JPG'))
        return Himage1



#打印地址信息
def printLocation(Locationget,Himage,draw,nwx=160,nwy=445):
    try:
        global f_open_list
        #获取的数据
        LocationGitFlag = Locationget[0]
        sds = Locationget[1]
        #打印地理位置图标

        piclocation = Image.open(os.path.join(picdir, 'location.png'))
        f_open_list.append(piclocation)
        Himage.paste(piclocation, (nwx,nwy-12), piclocation)
        #
        if(LocationGitFlag == 1):    
            cityname =sds['city']#城市名称
            adcode =sds['adcode']#城市代码
            
            #地理位置（精确到城市）
            draw.text((nwx+35, nwy), cityname, font = font22, fill = white)
        else:
            #错误信息
            draw.text((nwx+35, nwy), "无信息", font = font22, fill = white)
            
    except Exception as err:
        #错误信息
        draw.text((nwx+35, nwy), "出错了", font = font22, fill = white)
        logging.error("the location info printed goes wrong")
        logging.exception(err)
    

#打印天气信息
def printWeather(weatherget,Himage,draw,nwx=183,nwy=0,width=617,height=126):#nwx=183,nwy=0,width=617,height=126
    try:
        global f_open_list
        #获取的数据
        WitherGitFlag = weatherget[0]
        sds = weatherget[1]

        #分割条
        divid_line_x = int(nwx+width*0.23)
        divid_line_y1 = int(nwy + height/2 - height*0.27)
        divid_line_y2 = int(nwy + height/2 + height*0.27)
        divid_line_width = int(0.005*width)
        if divid_line_width<1:divid_line_width=1
        draw.line((divid_line_x, divid_line_y1, divid_line_x, divid_line_y2), fill = black_b,width = divid_line_width)

        
        #获取天气的情况
        if(WitherGitFlag == 1):
            tempMax =sds['daily'][0]['tempMax']
            tempMin =sds['daily'][0]['tempMin']
            nowtemp =sds['daily'][0]['fxDate']
            weathericon = sds['daily'][0]['iconDay']
            weathertext = sds['daily'][0]['textDay']
            
            UV = sds['daily'][0]['uvIndex']
            wet = sds['daily'][0]['humidity']
            vis = sds['daily'][0]['vis'] #能见度
            
            #文字
            text_x = int(divid_line_x + width*0.07)
            text_y = int(nwy+0.08*height)
            fontnumb = 20
            fontfont = font20
            draw.text((text_x, int(height/4*0+height/8-10)), "实时", font = font20, fill = black_b)
            draw.text((text_x, int(height/4*1+height/8-10)), "温度", font = font20, fill = black_b)
            draw.text((text_x, int(height/4*2+height/8-10)), "湿度", font = font20, fill = black_b)
            draw.text((text_x, int(height/4*3+height/8-10)), " UVI", font = font20, fill = black_b)
        
            
            #横线圆球滑条
            Slidebar_x = int(text_x + 0.12*width)
            Slidebar_width = int(width*0.5)
            Slidebar_ball_r = int(height*0.08)
            Slidebar_line_width = int(Slidebar_ball_r/3)
            drawSlidebar(x=Slidebar_x,y=int(height/4*1+height/8),width=Slidebar_width,draw=draw,linewidth=Slidebar_line_width,r=Slidebar_ball_r,num=nowtemp,startnum=tempMin,stopnum=tempMax,fontsize=12,color=black_b)
            drawSlidebar(x=Slidebar_x,y=int(height/4*2+height/8),width=Slidebar_width,draw=draw,linewidth=Slidebar_line_width,r=Slidebar_ball_r,num=wet,startnum=0,stopnum=100,fontsize=12,color=black_b)
            drawSlidebar(x=Slidebar_x,y=int(height/4*3+height/8),width=Slidebar_width,draw=draw,linewidth=Slidebar_line_width,r=Slidebar_ball_r,num=UV,startnum=0,stopnum=15,fontsize=12,color=black_b)
            

            #实时能见度
            RoundedRectangle_x = Slidebar_x
            RoundedRectangle_y = int(height/16)
            RoundedRectangle_width = int(width/11)
            if RoundedRectangle_width<70:RoundedRectangle_width=70
            RoundedRectangle_height = int(height/8)
            if RoundedRectangle_height<20:RoundedRectangle_height=20
            drawRoundedRectangle(RoundedRectangle_x,RoundedRectangle_y,RoundedRectangle_width,RoundedRectangle_height,3,black_b,draw)
            text_x = int(RoundedRectangle_x + RoundedRectangle_width/2 - len(vis+'km')*20/2/2)
            text_y = int(RoundedRectangle_y + RoundedRectangle_height/2 - 10 )
            draw.text((text_x, text_y), vis+'km', font = font20, fill = white)


            #打印天气图标
            pic_size = int(height*0.62)
            iconNo = weathericon + '.png'
            pic = Image.open(os.path.join(weathericondir, iconNo)).convert('RGBA')
            f_open_list.append(pic)
            pic_resize = pic.resize((pic_size,pic_size))
            pic_x =int(nwx + (divid_line_x - nwx)/2 - pic_size/2)
            pic_y = text_y

            Himage.paste(pic_resize, (pic_x,pic_y), pic_resize)#保持图片在框的中心
            

            #打印天气文字
            text_x = int(nwx + (divid_line_x - nwx)/2 -len(weathertext)*24/2)#字体是24号,保持文字居中
            text_y = int(pic_y + pic_size*1.1)
            draw.text((text_x,text_y),weathertext,font = font24,fill = black_b)
            
            
            

            
   
            logging.info("the wither showed successfully")
        else:
            #天气获取出错后重新获取
            draw.text((int(divid_line_x*1.1), divid_line_y1), "天气信息出错", font = font24, fill = black_b)
            
    except Exception as err:
        logging.error("the wither info printed goes wrong")
        logging.exception(err)
        
        
#打印时间信息
def printTime(timeget,lastMin,lastHour,draw,nwx = 280,nwy = 442):

    try:
        #获取所有信息
        nowMin = timeget[0]
        nowHour = timeget[1]
        nowDay = timeget[2].strip()
        nowTime = timeget[3]
        nowWeek = timeget[4]
        CNcalender_day = timeget[5]
        CNcalender_month = timeget[6]
        CNcalender_date = timeget[7]

        #打印log信息
        logging.info("now min {}, last min {}".format(nowMin,lastMin))
        logging.info("now hour {}, last hour {}".format(nowHour,lastHour))

        #打印系统时间
        draw.text((nwx, nwy), nowDay, font = font24, fill = white) #阳历
        draw.text((nwx+(len(nowDay))*12, nwy), CNcalender_day, font = font24, fill = white) #农历
        draw.text((nwx+(len(nowDay))*12+(len(CNcalender_day)+1)*24, nwy), nowWeek, font = font24, fill = white) #星期
        draw.text((nwx+(len(nowDay))*12+(len(CNcalender_day)+1)*24+(len(nowWeek)+1)*24, nwy), nowTime, font = font24, fill = white) #时间

        #输出logging info
        logging.info("the time info is correct")
    except Exception as err:
        #如果没有获取到时间信息
        logging.error("the time info goes wrong")
        logging.exception(err)
        draw.text((nwx, nwy), "时间信息出错", font = font48, fill = white)
        
#打印电量信息
def printBattery(batteryget,draw,percent=1,centerx=115,centery=456):

    try:
        ##获取的数据
        bus_voltage = batteryget[0]
        p = batteryget[1]
        chargingFlag = batteryget[2]
        current = batteryget[3]
        ##基础变量位置变量
        startx=int(centerx-34*percent)
        starty=int(centery-15*percent)
        stopx=int(centerx+34*percent)
        stopy=int(centery+15*percent)
        gap = int((stopx - startx)/5*0.15)
        long = int((stopx - startx)/5*0.7)
        centery1 = int(starty+(stopy-starty)/2-(stopy-starty)/6)
        centery2 = int(starty+(stopy-starty)/2+(stopy-starty)/6)
        #绘制电池图标
        draw.rectangle((startx, starty, stopx, stopy), outline = black_b, fill = black_b)# 整体电池框（纯黑）
        draw.rectangle((stopx, centery1 , stopx+2*gap, centery2), outline = white, fill = black_b)# 电池正极突起
        
        draw.rectangle((startx+1*gap+0*long, starty+3*gap, startx+1*gap+1*long, stopy-3*gap), outline = white, fill = white)#0-20
        draw.rectangle((startx+3*gap+1*long, starty+3*gap, startx+3*gap+2*long, stopy-3*gap), outline = white, fill = white)#20-40
        draw.rectangle((startx+5*gap+2*long, starty+3*gap, startx+5*gap+3*long, stopy-3*gap), outline = white, fill = white)#40-60
        draw.rectangle((startx+7*gap+3*long, starty+3*gap, startx+7*gap+4*long, stopy-3*gap), outline = white, fill = white)#60-80
        draw.rectangle((startx+9*gap+4*long, starty+3*gap, startx+9*gap+5*long, stopy-3*gap), outline = white, fill = white)#80-100
        if p<80:
                draw.rectangle((startx+9*gap+4*long, starty+3*gap, startx+9*gap+5*long, stopy-3*gap), outline = white, fill = black_b)#80-100
                if p<60:
                    draw.rectangle((startx+7*gap+3*long, starty+3*gap, startx+7*gap+4*long, stopy-3*gap), outline = white, fill = black_b)#60-80
                    if p<40:
                        draw.rectangle((startx+5*gap+2*long, starty+3*gap, startx+5*gap+3*long, stopy-3*gap), outline = white, fill = black_b)#40-60
                        if p<20:
                            draw.rectangle((startx+3*gap+1*long, starty+3*gap, startx+3*gap+2*long, stopy-3*gap), outline = white, fill = black_b)#20-40
                            if p<10:
                                draw.rectangle((startx+1*gap+0*long, starty+3*gap, startx+1*gap+1*long, stopy-3*gap), outline = white, fill = black_b)#0-20
        draw.text((centerx-4*(len(str(int(p)))+1), stopy-6),str(int(p))+'%',font = font12,fill = white)#电池电量
        #输出logging info
        logging.info("the battery info gitted successfully")
        logging.info("now battery voltage:{} ,now battery life: {:3.1f}%".format(bus_voltage,p))
        #确定是否充电
        if(chargingFlag == 1 and not p == 150):#充电且没有错误码
            
            draw.line((startx, starty, stopx, starty), fill = white)#电池框白线
            #draw.text((110, 440), '{:3.1f}'.format(p), font = font20, fill = black_b)#充电电压会多0.2v
            logging.info("charging, now current {:6.2f}mA input".format(-current))
        elif(chargingFlag == 0 and not p == 150):#没有充电且没有错误码
            #draw.rectangle((100, 440, 180, 470), outline = white, fill = white)
            #draw.text((110, 440), '{:3.1f}'.format(p), font = font20, fill = black_b)
            logging.info("not charging, now current {:6.2f}mA output".format(current))
        elif(p == 150):#错误码
            #draw.rectangle((100, 440, 180, 470), outline = white, fill = black_b)
            #draw.text((110, 440), '电量x', font = font20, fill = black_b)
            draw.line((startx, starty, stopx, stopy), fill = white, width = 2)#画个X
            draw.line((startx, stopy, stopx, starty), fill = white, width = 2)#画个X
            logging.info("charging message goes wrong")
        #输出消耗电量
        #logging.info("battery consumed {:6.2f}mAh".format(powerConsumed))
            
        #低电量关机操作
        if(p<=3):
            logging.info("the battery is very low, the system will shut down")
            draw.line((startx, starty, stopx, stopy), fill = white, width = 2)#画个X
            draw.line((startx, stopy, stopx, starty), fill = white, width = 2)#画个X
            time.sleep(100)
            os.system("shutdown -t 5 now")
            sys.exit()
            time.sleep(10)
    except Exception as err:
        #如果没有正常打印电量信息
        logging.error("the battery info goes wrong")
        logging.exception(err)
        draw.text((370, 400), '电量信息出错', font = font24, fill = white)


#画课表
def drawclasslist(classconf,classlist,timeget,draw,nwx=183,nwy=129,width=183,height=304):#nwx=183,nwy=129,width=183,height=304
    
    

    #绘图
    Rectangle_x = int(nwx + width/2 - width*0.4)
    Rectangle_y = int(nwy + height/7)
    step = int(height*0.28)
    Rectangle_width = int(width*0.8)
    Rectangle_height = int(height*0.23)
    Rectangle_r = int(width*0.05)
    if Rectangle_r<5:Rectangle_r=5
    error = int(Rectangle_r/2)

    line_x1 = int(nwx + width/2 - width*0.3)
    line_x2 = int(nwx + width/2 + width*0.3)
    line_y = int(Rectangle_y + Rectangle_height/2)
    line_step = step
    line_width = error

    drawRoundedRectangle(Rectangle_x,Rectangle_y+step*0,Rectangle_width,Rectangle_height,Rectangle_r,black_b,draw)##依次是： 起始x，起始y，矩形宽，矩形高，矩形圆角半径，绘图
    drawRoundedRectangle(Rectangle_x+error,Rectangle_y+step*0+error,Rectangle_width-error,Rectangle_height-error,Rectangle_r,white,draw)
    draw.line((line_x1, line_y+line_step*0, line_x2, line_y+line_step*0), fill = black_b, width = line_width)
    
    drawRoundedRectangle(Rectangle_x,Rectangle_y+step*1,Rectangle_width,Rectangle_height,Rectangle_r,black_b,draw)
    drawRoundedRectangle(Rectangle_x+error,Rectangle_y+step*1+error,Rectangle_width-error,Rectangle_height-error,Rectangle_r,white,draw)
    draw.line((line_x1, line_y+line_step*1, line_x2, line_y+line_step*1), fill = black_b, width = line_width)
    
    drawRoundedRectangle(Rectangle_x,Rectangle_y+step*2,Rectangle_width,Rectangle_height,Rectangle_r,black_b,draw)
    drawRoundedRectangle(Rectangle_x+error,Rectangle_y+step*2+error,Rectangle_width-error,Rectangle_height-error,Rectangle_r,white,draw)
    draw.line((line_x1, line_y+line_step*2, line_x2, line_y+line_step*2), fill = black_b, width = line_width)
    try:
        #计算
        #timeget，0是nowmin，1是nowhour，2是nowDay，3是nowTime，4是星期
        #计算与第一周第一天相差的天数推断这是第几周
        dict = {"星期一":1,"星期二":2,"星期三":3,"星期四":4,"星期五":5,"星期六":6,"星期日":7}
        startweekMon = classconf['startmonday']
        nowday=timeget[2]
        ys = int(startweekMon.split('-')[0])
        ms = int(startweekMon.split('-')[1])
        ds = int(startweekMon.split('-')[2])
        yn = int(nowday.split('-')[0])
        mn = int(nowday.split('-')[1])
        dn = int(nowday.split('-')[2])
        d1 = datetime.datetime(ys,ms,ds)
        d2 = datetime.datetime(yn,mn,dn)
        interval = d2-d1
        intervaldays = interval.days+1
        nowweek = int((intervaldays-dict.get(timeget[4]))/7)+1
        week_text_y = int(nwy+(Rectangle_y-nwy)/2-12)
        draw.text((line_x1,week_text_y),'第{}周/{}周'.format(nowweek,classconf['weeks']),font=font24,fill = black_b)
        ##周数：nowweek，周几（数字）：dict.get(timeget[4])
        
        #判断这天有什么课
        center_error = int(Rectangle_height/4)
        for classes in classlist.keys():
            a=int(nowweek)
            if a in classlist[classes]['classweek']:#如果这周上这节课
                if dict.get(timeget[4]) == classlist[classes]['classday']:#如果这天上这节课
                    logging.info("have class")
                    for i in classlist[classes]['classnum']:
                        if i == 1:
                            texty = line_y+line_step*0 - center_error - 6
                        if i == 2:
                            texty = line_y+line_step*0 + center_error - 6
                        if i == 3:
                            texty = line_y+line_step*1 - center_error - 6
                        if i == 4:
                            texty = line_y+line_step*1 + center_error - 6
                        if i == 5:
                            texty = line_y+line_step*2 - center_error - 6
                        draw.text((line_x1,texty),'{},{}'.format(classlist[classes]['classname'],classlist[classes]['place']),font=font14,fill = black_b)
    except Exception as err:
        #如果没有正常打印课表信息
        logging.error("the classlist info goes wrong")
        logging.exception(err)
        draw.text((212, 135), '课表出错XX', font = font24, fill = black_b)
            
            
#画todolist
def drawToDolist(todolist,timeget,draw,nwx=0,nwy=0,width=183,height=432):
    #标题
    draw.text((30,12),"ToDo List",font = font28,fill = black_b)
    try:
        #计算DDl和今天距离19700101的天数并作为新的键值对插入字典
        startday = '1970-01-01'
        yf = int(startday.split('-')[0])
        mf = int(startday.split('-')[1])
        df = int(startday.split('-')[2])
        d0 = datetime.datetime(yf,mf,df)
        
        nowday=timeget[2]#今日，备用
        yn = int(nowday.split('-')[0])
        mn = int(nowday.split('-')[1])
        dn = int(nowday.split('-')[2])
        d1 = datetime.datetime(yn,mn,dn)
        d1d0 = (d1-d0).days
        for item in todolist:
            if item['DDl'] == "1970-01-01":
                item['DDl'] = nowday
            yd = int(item['DDl'].split('-')[0])
            md = int(item['DDl'].split('-')[1])
            dd = int(item['DDl'].split('-')[2])
            dx = datetime.datetime(yd,md,dd)
            dxx = dx - d0
            item['days']=dxx.days
        #对列表重新排序，按days由小到大排序
        todolist = sorted(todolist, key = lambda list1:list1['days'])
        
        #开始
        n=0#标志这是第几个
        for item in todolist:
            if item['checkbox'] == False:
                logging.info(item)
                
                #测定字符宽度，中文字符一个宽度为两个英文字符宽度，以英文字符计算
                len1 = 0 #总字符宽度
                ch = 0 #中文字个数
                
                for i in list(item['name']):
                    if '\u4e00' <= i <= '\u9fff':
                        len1 = len1 + 2
                        ch = ch+1
                    else:
                        len1 = len1 +1
                    if len1>=8:#超出8个字符就不计算了
                        break
                #计算实际字符数，舍去过长的
                if len1>=8:
                    x = ch+(len1-2*ch)
                    item['name']=item['name'][0:x]+'...'
                    
                    
                if d1d0<item['days'] and n<5:#如果ddl还没到
                    drawRoundedRectangle(17,55+n*70,150,50,4,black_b,draw)#正常黑色边框
                    drawRoundedRectangle(19,57+n*70,146,46,4,white,draw)#正常白色提醒
                    
                    
                    #任务名和ddl    
                    draw.text((25,60+n*70),item['name'],font = font24,fill = black_b)#
                    #如果ddl是今天，加上today标志
                    if d1d0==item['days']:
                        draw.text((25,90+n*70),'ddl: '+item['DDl']+' today',font = font12,fill = black_b)
                    else:
                        draw.text((25,90+n*70),'ddl: '+item['DDl'],font = font12,fill = black_b)
                    #是否加星
                    if item['star'] == 'star':
                        #加星情况下
                        drawRoundedRectangle(147,72+n*70,12,12,2,black_b,draw)#白底黑星
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = white)#白字
                    else:
                        #不加星情况
                        drawRoundedRectangle(147,72+n*70,12,12,2,black_b,draw)#白底黑框，黑框内还是白底
                        drawRoundedRectangle(148,73+n*70,10,10,2,white,draw)
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = black_b)#黑字
                    
                    
                    
                elif d1d0>=item['days'] and n<5:#如果ddl已经到了
                    drawRoundedRectangle(17,55+n*70,150,50,4,black_b,draw)#黑色醒目提醒
                    
                    
                        
                    draw.text((25,60+n*70),item['name'],font = font24,fill = white)#
                    if d1d0==item['days']:
                        draw.text((25,90+n*70),'ddl: '+item['DDl']+' today',font = font12,fill = white)
                    else:
                        draw.text((25,90+n*70),'ddl: '+item['DDl'],font = font12,fill = white)
                    
                    if item['star'] == 'star':
                        #加星情况下
                        drawRoundedRectangle(147,72+n*70,12,12,2,white,draw)#黑底白星
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = black_b)#黑字
                    else:
                        #不加星情况
                        drawRoundedRectangle(147,72+n*70,12,12,2,white,draw)#黑底白框，白框内还是黑底
                        drawRoundedRectangle(148,73+n*70,10,10,2,black_b,draw)
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = white)#白字
                
                #下一个计数
                n=n+1
        if n>=5:
            release = n-5
            draw.text((40,400),'剩余'+str(release)+'个任务',font = font20,fill = black_b)#
    except Exception as err:
        #如果没有正常打印课表信息
        logging.error("the todolist info goes wrong")
        logging.exception(err)
        draw.text((10, 135), 'todo 出错', font = font24, fill = black_b)
    
    