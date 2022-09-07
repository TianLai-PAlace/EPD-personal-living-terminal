from Conf import *


#画滑条
def drawSlidebar(x,y,width,draw,linewidth=2,r=10,num=50,startnum=0,stopnum=100,fontsize=20,color=0):
    #依次是：直线起始x，直线起始y，直线长度，绘图父元素，直线宽度，圆半径，使用值，起始值，停止值，使用字号，颜色（0黑255白）
    #设置反色
    if color == 255:
        recolor = 0
    if color == 0:
        recolor = 255
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
                     color:int,
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
    #draw.arc((50,440,80,470), start = 225, end = 315, fill = 255)
    logging.info("wifi drawed")
    wifi = Image.open(os.path.join(picdir, 'wifi.bmp'))
    Himage.paste(wifi, (nwx,nwy))
    if not net:
        draw.line((nwx,nwy,nwx+48,nwy+48),fill=255,width=3)
        

#打印图片（之后会联网获取）
def printpic(Himage,draw,net,nwx=366,nwy=144):
    try:
        if not net:
            draw.text((nwx+20,nwy+20),'ERROR-设备未联网',fill = 0,font = font28)
            draw.text((nwx+20,nwy+60),'请连接设备热点为设备配网',fill = 0,font = font28)
            draw.text((nwx+20,nwy+120),'热点名： TLPA-AP-xxx',fill = 0,font = font28)
            draw.text((nwx+20,nwy+160),'设备将在5分钟内联网回复',fill = 0,font = font28)
        else:
            logging.info("picture drawed")
            #随机挑选一张图片展示
            pic = random.choice(photolist)
            
            #获取图片长宽并计算长宽比
            long,width = pic.size
            lwrato = float(long/width)#图片长宽比
            lwrato_ori = float(395/276)#展示框长宽比
            
            #计算图片长宽比和展示框长宽比的差
            value_difference = lwrato - lwrato_ori
            
            #计算差的绝对值
            if value_difference < 0:
                absolute_value_difference = -value_difference
            else:
                absolute_value_difference = value_difference
            
            #如果二者长宽比相差不大，就直接resize
            if absolute_value_difference<=0.3:
                pic_resize = pic.resize((395,276))
                pic = pic_resize.convert("1")
                Himage.paste(pic, (nwx,nwy))
            
            #如果二者长宽比相差较大且原图像更倾向于竖向
            elif absolute_value_difference>0.3 and value_difference<-0.3:
                long_r = int(276*lwrato)
                width_r = 276
                pic_resize = pic.resize((long_r,width_r))#不改变长宽比的情况下改变图片大小
                pic = pic_resize.convert("1")
                Himage.paste(pic, (int(nwx+395/2-long_r/2),nwy))#图片中心放置
                
            #如果二者长宽比相差较大且原图像更长
            elif absolute_value_difference>0.3 and value_difference>0.3:
                long_r = 395
                width_r = 276
                pic_resize = pic.resize((int(276*lwrato),276))#不改变长宽比的情况下将图片高度适配相框高度
                pic_crop = pic_resize((int((276*lwrato)/2-395/2),0,int((276*lwrato)/2-395/2),276))#截取长图中间部分
                pic = pic_crop.convert("1")
                Himage.paste(pic, (nwx,nwy))
                
            
    except Exception as err:
        #draw.text((nwx, nwy), "出错了", font = font48, fill = 0)
        drawtextautoline(nwx,
                     nwy,
                     err,
                     font24,
                     24,
                     390,
                     0,draw)
        logging.error("the photo  printed goes wrong")
        logging.exception(err)



#打印地址信息
def printLocation(Locationget,Himage,draw,nwx=160,nwy=445):
    try:
        #获取的数据
        LocationGitFlag = Locationget[0]
        sds = Locationget[1]
        #打印地理位置图标
        piclocation = Image.open(os.path.join(picdir, 'location.bmp'))
        Himage.paste(piclocation, (nwx,nwy-12))
        #
        if(LocationGitFlag == 1):    
            cityname =sds['city']#城市名称
            adcode =sds['adcode']#城市代码
            
            #地理位置（精确到城市）
            draw.text((nwx+35, nwy), cityname, font = font22, fill = 255)
        else:
            #错误信息
            draw.text((nwx+35, nwy), "无信息", font = font22, fill = 255)
            
    except Exception as err:
        #错误信息
        draw.text((nwx+35, nwy), "出错了", font = font22, fill = 255)
        logging.error("the location info printed goes wrong")
        logging.exception(err)
    

#打印天气信息
def printWeather(weatherget,Himage,draw):
    try:
        #获取的数据
        WitherGitFlag = weatherget[0]
        sds = weatherget[1]

        
        #
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
            draw.text((366, 10), "实时", font = font20, fill = 0)
            draw.text((366, 40), "温度", font = font20, fill = 0)
            draw.text((366, 70), "湿度", font = font20, fill = 0)
            draw.text((366, 100), " UVI", font = font20, fill = 0)
            
            #实时能见度
            drawRoundedRectangle(420,8,68,24,3,0,draw)
            draw.text((430, 9), vis+'km', font = font20, fill = 255)
            
            #横线圆球滑条
            drawSlidebar(x=440,y=50,width=310,draw=draw,linewidth=3,r=10,num=nowtemp,startnum=tempMin,stopnum=tempMax,fontsize=12,color=0)
            drawSlidebar(x=440,y=80,width=310,draw=draw,linewidth=3,r=10,num=wet,startnum=0,stopnum=100,fontsize=12,color=0)
            drawSlidebar(x=440,y=110,width=310,draw=draw,linewidth=3,r=10,num=UV,startnum=0,stopnum=15,fontsize=12,color=0)
            
            
            #打印天气图标
            pic_size = 80
            iconNo = weathericon + '.jpg'
            pic = Image.open(os.path.join(weathericondir, iconNo))
            pic_resize = pic.resize((pic_size,pic_size))
            Himage.paste(pic_resize, (int(254-pic_size/2),10))#保持图片在框的中心
            
            #打印天气文字
            text_x = int(254-len(weathertext)*24/2)#字体是24号,保持文字居中
            text_y = 90
            draw.text((text_x,text_y),weathertext,font = font24,fill = 0)
            
            
            

            
   
            logging.info("the wither showed successfully")
        else:
            #天气获取出错后重新获取
            draw.text((370, 60), "天气信息出错", font = font24, fill = 0)
            
    except Exception as err:
        logging.error("the wither info printed goes wrong")
        logging.exception(err)
        
        
#打印时间信息
def printTime(timeget,lastMin,lastHour,draw,startx = 460,centery = 456):

    try:
        nowMin = timeget[0]
        nowHour = timeget[1]
        nowDay = timeget[2]
        nowTime = timeget[3]
        nowWeek = timeget[4]
        #打印log信息
        logging.info("now min {}, last min {}".format(nowMin,lastMin))
        logging.info("now hour {}, last hour {}".format(nowHour,lastHour))
        #打印系统时间
        draw.text((startx, centery-12), nowDay, font = font24, fill = 255)
        draw.text((startx+(len(nowDay)+0)*12, centery-11), nowWeek, font = font22, fill = 255)
        draw.text((startx+(len(nowDay)+0+2*len(nowWeek)+1)*12, centery-12), nowTime, font = font24, fill = 255)

        #输出logging info
        logging.info("the time info is correct")
    except Exception as err:
        #如果没有获取到时间信息
        logging.error("the time info goes wrong")
        logging.exception(err)
        draw.text((420, 200), "时间信息出错", font = font48, fill = 255)
        
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
        draw.rectangle((startx, starty, stopx, stopy), outline = 0, fill = 0)# 整体电池框（纯黑）
        draw.rectangle((stopx, centery1 , stopx+2*gap, centery2), outline = 255, fill = 0)# 电池正极突起
        
        draw.rectangle((startx+1*gap+0*long, starty+3*gap, startx+1*gap+1*long, stopy-3*gap), outline = 255, fill = 255)#0-20
        draw.rectangle((startx+3*gap+1*long, starty+3*gap, startx+3*gap+2*long, stopy-3*gap), outline = 255, fill = 255)#20-40
        draw.rectangle((startx+5*gap+2*long, starty+3*gap, startx+5*gap+3*long, stopy-3*gap), outline = 255, fill = 255)#40-60
        draw.rectangle((startx+7*gap+3*long, starty+3*gap, startx+7*gap+4*long, stopy-3*gap), outline = 255, fill = 255)#60-80
        draw.rectangle((startx+9*gap+4*long, starty+3*gap, startx+9*gap+5*long, stopy-3*gap), outline = 255, fill = 255)#80-100
        if p<80:
                draw.rectangle((startx+9*gap+4*long, starty+3*gap, startx+9*gap+5*long, stopy-3*gap), outline = 255, fill = 0)#80-100
                if p<60:
                    draw.rectangle((startx+7*gap+3*long, starty+3*gap, startx+7*gap+4*long, stopy-3*gap), outline = 255, fill = 0)#60-80
                    if p<40:
                        draw.rectangle((startx+5*gap+2*long, starty+3*gap, startx+5*gap+3*long, stopy-3*gap), outline = 255, fill = 0)#40-60
                        if p<20:
                            draw.rectangle((startx+3*gap+1*long, starty+3*gap, startx+3*gap+2*long, stopy-3*gap), outline = 255, fill = 0)#20-40
                            if p<10:
                                draw.rectangle((startx+1*gap+0*long, starty+3*gap, startx+1*gap+1*long, stopy-3*gap), outline = 255, fill = 0)#0-20
        draw.text((centerx-4*(len(str(int(p)))+1), stopy-6),str(int(p))+'%',font = font12,fill = 255)#电池电量
        #输出logging info
        logging.info("the battery info gitted successfully")
        logging.info("now battery voltage:{} ,now battery life: {:3.1f}%".format(bus_voltage,p))
        #确定是否充电
        if(chargingFlag == 1 and not p == 150):#充电且没有错误码
            
            draw.line((startx, starty, stopx, starty), fill = 255)#电池框白线
            #draw.text((110, 440), '{:3.1f}'.format(p), font = font20, fill = 0)#充电电压会多0.2v
            logging.info("charging, now current {:6.2f}mA input".format(-current))
        elif(chargingFlag == 0 and not p == 150):#没有充电且没有错误码
            #draw.rectangle((100, 440, 180, 470), outline = 255, fill = 255)
            #draw.text((110, 440), '{:3.1f}'.format(p), font = font20, fill = 0)
            logging.info("not charging, now current {:6.2f}mA output".format(current))
        elif(p == 150):#错误码
            #draw.rectangle((100, 440, 180, 470), outline = 255, fill = 0)
            #draw.text((110, 440), '电量x', font = font20, fill = 0)
            draw.line((startx, starty, stopx, stopy), fill = 255, width = 2)#画个X
            draw.line((startx, stopy, stopx, starty), fill = 255, width = 2)#画个X
            logging.info("charging message goes wrong")
        #输出消耗电量
        #logging.info("battery consumed {:6.2f}mAh".format(powerConsumed))
            
        #低电量关机操作
        if(p<=3):
            logging.info("the battery is very low, the system will shut down")
            draw.line((startx, starty, stopx, stopy), fill = 255, width = 2)#画个X
            draw.line((startx, stopy, stopx, starty), fill = 255, width = 2)#画个X
            time.sleep(100)
            os.system("shutdown -t 5 now")
            sys.exit()
            time.sleep(10)
    except Exception as err:
        #如果没有正常打印电量信息
        logging.error("the battery info goes wrong")
        logging.exception(err)
        draw.text((370, 400), '电量信息出错', font = font24, fill = 255)


#画课表
def drawclasslist(classconf,classlist,timeget,draw):
    
    

    #绘图
    
    
    drawRoundedRectangle(213,174,114,74,5,0,draw)##依次是： 起始x，起始y，矩形宽，矩形高，矩形圆角半径，绘图
    drawRoundedRectangle(216,177,111,71,5,255,draw)
    draw.line((226, 212, 313, 212), fill = 0, width = 2)
    
    drawRoundedRectangle(213,259,114,74,5,0,draw)
    drawRoundedRectangle(216,262,111,71,5,255,draw)
    draw.line((226, 296, 313, 296), fill = 0, width = 2)
    
    drawRoundedRectangle(213,345,114,74,5,0,draw)
    drawRoundedRectangle(216,348,111,71,5,255,draw)
    draw.line((226, 382, 313, 382), fill = 0, width = 2)
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
        draw.text((212,135),'第{}周/{}周'.format(nowweek,classconf['weeks']),font=font24,fill=0)
        ##周数：nowweek，周几（数字）：dict.get(timeget[4])
        
        #判断这天有什么课
        for classes in classlist.keys():
            a=int(nowweek)
            if a in classlist[classes]['classweek']:#如果这周上这节课
                if dict.get(timeget[4]) == classlist[classes]['classday']:#如果这天上这节课
                    logging.info("have class")
                    for i in classlist[classes]['classnum']:
                        if i == 1:
                            texty = 188
                        if i == 2:
                            texty = 218
                        if i == 3:
                            texty = 269
                        if i == 4:
                            texty = 301
                        if i == 5:
                            texty = 357
                        draw.text((225,texty),'{},{}'.format(classlist[classes]['classname'],classlist[classes]['place']),font=font12,fill=0)
    except Exception as err:
        #如果没有正常打印课表信息
        logging.error("the classlist info goes wrong")
        logging.exception(err)
        draw.text((212, 135), '课表出错XX', font = font24, fill = 0)
            
            
#画todolist
def drawToDolist(todolist,timeget,draw):
    #标题
    draw.text((30,12),"ToDo List",font = font28,fill = 0)
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
                    drawRoundedRectangle(17,55+n*70,150,50,4,0,draw)#正常黑色边框
                    drawRoundedRectangle(19,57+n*70,146,46,4,255,draw)#正常白色提醒
                    
                    
                    #任务名和ddl    
                    draw.text((25,60+n*70),item['name'],font = font24,fill = 0)#
                    #如果ddl是今天，加上today标志
                    if d1d0==item['days']:
                        draw.text((25,90+n*70),'ddl: '+item['DDl']+' today',font = font12,fill = 0)
                    else:
                        draw.text((25,90+n*70),'ddl: '+item['DDl'],font = font12,fill = 0)
                    #是否加星
                    if item['star'] == 'star':
                        #加星情况下
                        drawRoundedRectangle(147,72+n*70,12,12,2,0,draw)#白底黑星
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = 255)#白字
                    else:
                        #不加星情况
                        drawRoundedRectangle(147,72+n*70,12,12,2,0,draw)#白底黑框，黑框内还是白底
                        drawRoundedRectangle(148,73+n*70,10,10,2,255,draw)
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = 0)#黑字
                    
                    
                    
                elif d1d0>=item['days'] and n<5:#如果ddl已经到了
                    drawRoundedRectangle(17,55+n*70,150,50,4,0,draw)#黑色醒目提醒
                    
                    
                        
                    draw.text((25,60+n*70),item['name'],font = font24,fill = 255)#
                    if d1d0==item['days']:
                        draw.text((25,90+n*70),'ddl: '+item['DDl']+' today',font = font12,fill = 255)
                    else:
                        draw.text((25,90+n*70),'ddl: '+item['DDl'],font = font12,fill = 255)
                    
                    if item['star'] == 'star':
                        #加星情况下
                        drawRoundedRectangle(147,72+n*70,12,12,2,255,draw)#黑底白星
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = 0)#黑字
                    else:
                        #不加星情况
                        drawRoundedRectangle(147,72+n*70,12,12,2,255,draw)#黑底白框，白框内还是黑底
                        drawRoundedRectangle(148,73+n*70,10,10,2,0,draw)
                        #重要程度
                        draw.text((150,72+n*70),item["importance"],font = font12,fill = 255)#白字
                
                #下一个计数
                n=n+1
        if n>=5:
            release = n-5
            draw.text((40,400),'剩余'+str(release)+'个任务',font = font20,fill = 0)#
    except Exception as err:
        #如果没有正常打印课表信息
        logging.error("the todolist info goes wrong")
        logging.exception(err)
        draw.text((10, 135), 'todo 出错', font = font24, fill = 0)
    
    