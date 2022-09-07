
from Conf import *
#ina219 = INA219.INA219(addr=0x43)

#获取所有图片列表
def getFileList(dir):
    photolist = []
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        if os.path.isdir(file):
            getFileList(file)
        elif os.path.isfile(file):
            pic = Image.open(os.path.join(photodir, file))
            photolist.append(pic)       
    return photolist


#获取时间
def getNowTime():
    #返回一个列表timeget，0是nowmin，1是nowhour，2是nowDay，3是nowTime，4是星期
    timeget=[]
    try:
        
        #菜勒公式计算当前的星期
        dict = {1:"星期一",2:"星期二",3:"星期三",4:"星期四",5:"星期五",6:"星期六",0:"星期日"}
        y = int(datetime.datetime.now().strftime('%Y'))
        m = int(datetime.datetime.now().strftime('%m'))
        d = int(datetime.datetime.now().strftime('%d'))
        if m == 1:
            m = 13
            y = y-1
        elif m == 2:
            m =14
            y = y-1
        allday = math.floor((y-1)+(y-1)/4-(y-1)/100+(y-1)/400+13*(m+1)/5+(m-1)*28-7+d)
        week = allday%7
        
        #农历
        numbermonth = {
            1 :"正",2 :"二",3 :"三",4 :"四",5 :"五",6 :"六",7 :"七",8 :"八",9 :"九",10:"十",11:"冬",12:"腊",
        }
        numberday = {
            1 :"初一",2 :"初二",3 :"初三",4 :"初四",5 :"初五",6 :"初六",7 :"初七",8 :"初八",9 :"初九",10:"初十",
            11:"十一",12:"十二",13:"十三",14:"十四",15:"十五",16:"十六",17:"十七",18:"十八",19:"十九",20:"廿十",
            21:"廿一",22:"廿二",23:"廿三",24:"廿四",25:"廿五",26:"廿六",27:"廿七",28:"廿八",29:"廿九",30:"卅十",
            31:"卅一",
            }
        today = LunarDate.today()
        chineseCalender = "农历"+numbermonth.get(today.month,"空")+"月"+numberday.get(today.day,"空")


        #导出所有日期相关内容
        timeget.append( int(datetime.datetime.now().strftime('%M')) )         #0 nowMin
        timeget.append( int(datetime.datetime.now().strftime('%H')) )         #1 nowHour
        timeget.append( datetime.datetime.now().strftime('%Y - %m - %d'))     #2 nowDay
        timeget.append( datetime.datetime.now().strftime('%H : %M') )         #3 nowTime
        timeget.append( dict.get(week,"出问题了") )                            #4 nowweekday
        timeget.append( chineseCalender )                                     #5 Chinese calender nowday
        timeget.append( today.month )                                         #6 Chinese calender nowmonth
        timeget.append( today.day )                                           #7 Chinese calender nowdate
        timeget.append( datetime.datetime.now().strftime('%m'))               #8 Solar calender nowmonth
        timeget.append( datetime.datetime.now().strftime('%d'))               #9 Solar calender nowday

        
    except Exception as err:
        logging.error("Time gitted goes wrong")
        logging.exception(err)
        timeget = []
        timeget.append(150)
        timeget.append(150)
        timeget.append('xx - xx - xx')
        timeget.append('xx : xx')
        timeget.append("出问题了")
        timeget.append( "一月初一" )
        timeget.append( "一" )
        timeget.append( "一" )
        timeget.append( "1" )
        timeget.append( "1" )
    return timeget

#获取电量
def getNowBattery():
    batteryget = []
    try:
        #获取电池电量
        # bus_voltage = ina219.getBusVoltage_V()   #获取电压
        # shunt_voltage = ina219.getShuntVoltage_mV() / 1000
        # current = ina219.getCurrent_mA()  #获取电流 充电为正，放电为负
        # power = ina219.getPower_W() #获取当前功率，单位 w， 或 V×A
        bus_voltage = userConf.bus_voltage   #获取电压
        shunt_voltage = userConf.shunt_voltage
        current = userConf.current  #获取电流 充电为正，放电为负
        power = userConf.power #获取当前功率，单位 w， 或 V×A

        p = (bus_voltage - shunt_voltage - 3.1)/1.1*100   #这是没有充电状态下的电量算法
        if(p > 100):p = 100
        if(p < 0):p = 0
        #判断是否充电
        if(current>0):
            chargingFlag = 1
            #logging.info('charging \n')
        elif(current <= 0):
            chargingFlag = 0
            #logging.info('not charging \n')
            
        batteryget.append(bus_voltage)       #获取电压,电压为batteryget[0]
        batteryget.append(p)                 #获取当前的电量，为batteryget[1]
        batteryget.append(chargingFlag)      #获取当前是否充电标志，为batteryget[2]
        batteryget.append(current)           #获取当前的电流，为batteryget[3]

    except Exception as err:
        logging.error("can not git the battery info")
        logging.exception(err)
        #p = 150 #150 错误码
        batteryget.append(150)       #获取电压,电压为batteryget[0]
        batteryget.append(150)       #获取当前的电量，为batteryget[1]
        batteryget.append(0)         #获取当前是否充电标志，为batteryget[2]
        batteryget.append(150)       #获取当前电流，为batteryget[3]
    return batteryget

#联网检查
def isNetOK(testserver):
    s = socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as err:
        logging.exception(err)
        return False

def isNetChinaOK(testserver=('www.baidu.com',443)):
    isOK = isNetOK(testserver)
    return isOK

NetNotConnectShowFlag = 0
NetConnected = False

def checkNet():
    ##联网检查模块
    testserver = [('www.bing.com',443),('www.baidu.com',443),('www.bilibili.com',443)]
    NetConnected=isNetChinaOK()#检测是否联网
    
    times_notconnect = 0 #重连次数
    
    while(not NetConnected):#没有联网的情况
        NetConnected=isNetChinaOK(testserver[times_notconnect%3])
        logging.error("wifi is not connected")
        times_notconnect = times_notconnect +1
        logging.info('times_notconnect: '+str(times_notconnect))
        if times_notconnect>=10:#连接超时情况
            return False
        time.sleep(1)
        #end while
    
    logging.info("wifi is connected")    #联网
    return True


#获取天气
@timeout_decorator.timeout(timeout_s)#超时直接报错
def getWeather(cityname,net):
    weatherget = []
    try:
        #没有联网情况下直接返回
        if not net:
            WitherGitFlag = 0#没有得到天气信息
            weatherget.append(WitherGitFlag)
            weatherget.append(defaultWeather)
            return weatherget
        ##把中文改成拼音
        name1 =''
        name = pypinyin.lazy_pinyin(cityname)
        for i in range(len(name)-1):
            name1 = name1+name[i]
        cityname=name1
        logging.info(cityname)
        ##通过名字获取locationid
        url2 = 'https://geoapi.qweather.com/v2/city/lookup?'
        value2 = {
            'location' : cityname,
            'key' : userConf.qweatherkey,
            'range': 'cn',
            'number': '1',
            'lang': 'en'
        }
        sd1 = requests.get(url2,params = value2)
        sds1 = sd1.json()#发送请
        locationid = sds1['location'][0]['id']
        logging.info(locationid)
        #改变locationid
        
        
        value['location']=locationid
        #获取天气
        sd = requests.get(url,params = value)
        sds = sd.json()#发送请求
        time.sleep(1)
        logging.info("the wither info is gitted")
        
        url3 = 'https://devapi.qweather.com/v7/weather/now?'
        value3 = {
            'location' : locationid,
            'key' : userConf.qweatherkey,
            #'lang' : 'en'
        }
        sd3 = requests.get(url3,params = value3)
        sds3 = sd3.json()#发送请
        
        #合并
        w = sds3['now']['temp']
        sds['daily'][0]['fxDate'] = w
        w = sds3['now']['vis']
        sds['daily'][0]['vis'] = w
        w = sds3['now']['humidity']
        sds['daily'][0]['humidity'] = w
        w = sds3['now']['icon']
        sds['daily'][0]['iconDay'] = w
        w = sds3['now']['text']
        sds['daily'][0]['textDay'] = w
        
        
        if(sds['code']=='200'):
            WitherGitFlag = 1  #得到天气信息
        else:
            WitherGitFlag = 0
        weatherget.append(WitherGitFlag) #是否得到天气标志，weatherget[0]
        
        weatherget.append(sds)           #所有天气信息，weatherget[1]
        
    except Exception as err:
        #如果没有获取到天气信息
        logging.error("the wither info gitting goes wrong")
        logging.exception(err)
        WitherGitFlag = 0#没有得到天气信息
        weatherget.append(WitherGitFlag)
        weatherget.append(defaultWeather)
    return weatherget

#获取位置
@timeout_decorator.timeout(timeout_s)#超时直接报错
def getLocation(net):
    Locationget = []
    try:
        #没联网情况直接返回
        if not net:
            Locationget.append(0)
            Locationget.append(defaultLocation)
            return Locationget
        #开始获取位置
        sd = requests.get(url1,params = value1)
        sds = sd.json()#发送请求
        #确定是否得到位置信息
        if(sds['status']):
            LocationGitFlag = 1  #得到位置信息
            logging.info("the location info is getted")
            Locationget.append(LocationGitFlag) #是否得到位置标志，weatherget[0]
            Locationget.append(sds)
            print(sds)
        else:
            LocationGitFlag = 0 #没有得到位置信息
            logging.info("the location info is not getted")
            logging.info(sds['info'])
            Locationget.append(LocationGitFlag) 
            Locationget.append(defaultLocation)
    
    except Exception as err:
        #如果获取到位置信息出错
        logging.error("the Location info gitting goes wrong")
        logging.exception(err)
        LocationGitFlag = 0#没有得到位置信息
        Locationget.append(LocationGitFlag)
        Locationget.append(defaultLocation)
    return Locationget

#获取todo list
@timeout_decorator.timeout(timeout_s)#超时直接报错
def getToDolist(net):
    #没网的情况：
    if not net:
        todolist = defaultToDolist
        return todolist
    #获取todolist
    true = True
    false = False
    null = False
    todolist = []
    try:
        response = requests.post(url_todo, json=payload_todo, headers=headers_todo)
        x = response.json()
        #找关键信息，再汇总成一个只由关键信息组成的字典列表
        
        for result in x["results"]:
            #一个一定有的数据
            
            checkbox = result["properties"]["Property"]["checkbox"]

            #四个个可能没有的数据和处理
            
            if not result["properties"]["任务名称"]["title"] == []:
                name = result["properties"]["任务名称"]["title"][0]["text"]["content"]
            else:
                name = "Undefined"
            
            if not result["properties"]["DDL"]["date"] == None:
                DDL = result["properties"]["DDL"]["date"]["start"]
            else:
                DDL = "1970-01-01"#在printfunction里这个值会被转换为nowday
                
            
            if not result["properties"]["star"]["select"] == None:
                star = result["properties"]["star"]["select"]["name"]
            else:
                star = "unstar"

            
            if not result["properties"]["importance"]["select"] == None:
                importance = result["properties"]["importance"]["select"]["name"]
            else:
                importance = "1"
                
            #加入列表
            todolist.append(
                {
                    'name': name,
                    'DDl': DDL,
                    'checkbox': checkbox,
                    'star':star,
                    'importance':importance

                }
            )
    except Exception as err:
        #获取出错的情况
        logging.info("to do list not get")
        logging.exception(err)
        todolist = defaultToDolist
    return todolist
        
def water_remind(last_time,set_time_min):
    set_time = set_time_min*60
    now_time = int(time.time())
    if now_time -last_time >= set_time:
        flag = True
    else:
        flag = False
    water_remind_list = []
    water_remind_list.append(flag)
    water_remind_list.append(now_time)
    return water_remind_list