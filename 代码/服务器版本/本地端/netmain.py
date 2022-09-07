
from io import BytesIO
###基础配置×××××××××××××××××××××××××××××××××××××××××××××××××××××××
from Conf import *


###信息获取函数部分×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

from getfunction import *

###信息打印函数部分×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

from printfunction import *


epd = epd7in5_V2.EPD()
while(1):
    try:
        #画板初始化
        Himage = Image.new('1', (800, 480), 255)
        draw = ImageDraw.Draw(Himage)
        
        #联网检查模块
        net = checkNet()
        printNet(Himage,draw,net)
        
        if(net):
        
            #获取服务器生成的图片
            url = 'http://43.136.213.29/output.jpg'
            value = {}
            res = requests.get(url,params=value)
            img = Image.open(BytesIO(res.content))

            #图片贴在画板上
            Himage.paste(img, (0,0))

            #Himage.save("D:\WorkingFiles\墨水屏\网络获取\output.jpg")
            
        
        #画实时的battery
        batteryget = getNowBattery()
        printBattery(batteryget,percent=1,draw=draw)
        
        
        

        #墨水屏初始化显示流程
        epd.init()
                    
        epd.Clear()

        time.sleep(1)

        epd.display(epd.getbuffer(Himage))

        time.sleep(1)

        epd.sleep()
        
        #两分钟执行一次
        time.sleep(120)
    except Exception as err:
        logging.error("the while 1 goes wrong")
        logging.exception(err)
        time.sleep(10)
        