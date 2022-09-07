
from Conf import *
ina219 = INA219.INA219(addr=0x43)

#获取时间
def getNowTime():
    #返回一个列表timeget，0是nowmin，1是nowhour，2是nowDay，3是nowTime，4是星期
    timeget=[]
    try:
        
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
        allday = math.floor((y-1)+(y-1)/4-(y-1)/100+(y-1)/400+13*(m+1)/5+(m-1)*28-7+d)#菜勒公式
        x = allday%7
        
        timeget.append( int(datetime.datetime.now().strftime('%M')) )#= nowMin
        timeget.append(int(datetime.datetime.now().strftime('%H')) )#nowHour
        timeget.append( datetime.datetime.now().strftime('%Y - %m - %d') )#nowDay =
        timeget.append( datetime.datetime.now().strftime('%H : %M') )#nowTime =
        timeget.append(dict.get(x,"出问题了"))#nowweekday =
        
    except Exception as err:
        logging.error("Time gitted goes wrong")
        logging.exception(err)
        timeget = []
        timeget.append(150)
        timeget.append(150)
        timeget.append('xx - xx - xx')
        timeget.append('xx : xx')
        timeget.append("出问题了")
    return timeget

#获取电量
def getNowBattery():
    batteryget = []
    try:
        #获取电池电量
        bus_voltage = ina219.getBusVoltage_V()   #获取电压
        shunt_voltage = ina219.getShuntVoltage_mV() / 1000
        current = ina219.getCurrent_mA()  #获取电流 充电为正，放电为负
        power = ina219.getPower_W() #获取当前功率，单位 w， 或 V×A

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
NetConnected = False;

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
@timeout_decorator.timeout(10)#超时直接报错
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
            'key' : 'c269ad4ed48a4a0387912cf6763087a5',
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
            'key' : 'c269ad4ed48a4a0387912cf6763087a5',
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
@timeout_decorator.timeout(10)#超时直接报错
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
        #确定是否得到天气信息
        if(sds['status']):
            LocationGitFlag = 1  #得到天气信息
            logging.info("the location info is getted")
            Locationget.append(LocationGitFlag) #是否得到天气标志，weatherget[0]
            Locationget.append(sds)
        else:
            LocationGitFlag = 0 #没有得到天气信息
            logging.info("the location info is not getted")
            logging.info(sds['info'])
            Locationget.append(LocationGitFlag) 
            Locationget.append(defaultLocation)
    
    except Exception as err:
        #如果获取到天气信息出错
        logging.error("the Location info gitting goes wrong")
        logging.exception(err)
        LocationGitFlag = 0#没有得到天气信息
        Locationget.append(LocationGitFlag)
        Locationget.append(defaultLocation)
    return Locationget

#获取todo list
@timeout_decorator.timeout(20)#超时直接报错
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
        
