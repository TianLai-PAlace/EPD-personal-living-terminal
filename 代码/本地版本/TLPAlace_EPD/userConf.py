#用户ip地址
userip = '117.173.139.98'

#和风天气userkey
qweatherkey = 'c269ad4ed48a4a0387912cf6763087a5'

#高德地图userkey
GaoDekey = '045668c0922d820f5a11761e8ad4946b'

#电池当前状态
bus_voltage = 4.0   #获取电压
shunt_voltage = 390 / 1000
current = 400  #获取电流 充电为正，放电为负
power = 0.201 #获取当前功率，单位 w， 或 V×A

#喝水提醒时间
water_drink_time = 10 #分钟

#notion todolist key
database_id='2c0125f0c3e64cc0b8f4564c0ff9392e'
Authorization="Bearer secret_gH2eurPILoRxIBl8MsVdlzmwnZCdqgSuTnYvNWh7cCC"

#生日信息
birthday = [
    {"name":"测试","calendar":"Chinese Calendar","month":7,"date":23},
    {"name":"妗妗","calendar":"Chinese Calendar","month":2,"date":4},#calender:"Chinese Calendar"农历、"Solar Calendar"阳历
    {"name":"老爸","calendar":"Chinese Calendar","month":2,"date":6},
    {"name":"雨姐","calendar":"Chinese Calendar","month":2,"date":29},
    {"name":"老妈","calendar":"Chinese Calendar","month":3,"date":8},
    {"name":"袁姐","calendar":"Chinese Calendar","month":4,"date":17},
    {"name":"舅舅","calendar":"Chinese Calendar","month":4,"date":15},
    {"name":"姥姥","calendar":"Chinese Calendar","month":11,"date":3},
    {"name":"我","calendar":"Solar Calendar","month":8,"date":25},
    {"name":"杨淳","calendar":"Solar Calendar","month":12,"date":9},
    {"name":"盛点","calendar":"Solar Calendar","month":3,"date":19},
    {"name":"李响","calendar":"Solar Calendar","month":5,"date":16},

]


#课表
# classconf = {
#     'startmonday':'2022-6-27', 课程开始的第一周
#     'weeks':'18' 本学期课程的周数
#     }
classconf = {
    'startmonday':'2022-8-29',
    'weeks':'18'    
    }

# 'class1':{                                       课程编号
#         'classname':'电子系统设计',               课程名称
#         'teachername':'none',                    老师名称
#         'place':'立B217',                        上课位置
#         'classweek':[1,2,5,9,10,11,12,13,14],   #上课的周数，连续上18周就[range(1,19)]
#         'classday':1,                           #周一到周日对应1到6 和 0
#         'classnum':[4]                          #上午两节下午两节晚上一节，分别对应1到5，该课表只针对大学一天五节课课表
#         },
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
        'classname':'EL',
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
        'classname':'S&S',
        'teachername':'AYNUL ISLAM',
        'place':'立B208',
        'classweek':[i for i in range(1,19)],
        'classday':3,
        'classnum':[3]
        },
    'class6':{
        'classname':'ED',
        'teachername':'Scott Roy',
        'place':'立B217',
        'classweek':[1,2,3,4,5,9,10,11,12,13,14],
        'classday':3,
        'classnum':[4]
        },
    'class7':{
        'classname':'EL',
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
        'classname':'ED',
        'teachername':'Scott Roy',
        'place':'立B217',
        'classweek':[3],
        'classday':4,
        'classnum':[4]
        },
    'class10':{
        'classname':'ESD',
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
        'classname':'S&S',
        'teachername':'AI',
        'place':'立B208',
        'classweek':[i for i in range(1,19)],
        'classday':5,
        'classnum':[2]
        },
    'class13':{
        'classname':'EL',
        'teachername':'sad',
        'place':'立B217',
        'classweek':[1,2,5,9,11,12,13],
        'classday':5,
        'classnum':[4]
        },
    'class14':{
        'classname':'none',
        'teachername':'ohh',
        'place':'宿舍',
        'classweek':[i for i in range(1,19)],
        'classday':6,
        'classnum':[1]
        },
    'class15':{
        'classname':'none',
        'teachername':'ohh',
        'place':'宿舍',
        'classweek':[i for i in range(1,19)],
        'classday':7,
        'classnum':[1]
        },
    'class16':{
        'classname':'ESD LAB',
        'teachername':'EN',
        'place':'科B330',
        'classweek':[5,10,12,14],
        'classday':5,
        'classnum':[5]
        },
    'class17':{
        'classname':'S&S LAB',
        'teachername':'EN',
        'place':'基础',
        'classweek':[9,10,12,14],
        'classday':3,
        'classnum':[5]
        },
    'class18':{
        'classname':'AI&ML LAB',
        'teachername':'EN',
        'place':'主A1-405',
        'classweek':[4,10,12,14],
        'classday':3,
        'classnum':[4]
        },
    'class19':{
        'classname':'ED LAB',
        'teachername':'EN',
        'place':'创新B416',
        'classweek':[5,9,13],
        'classday':4,
        'classnum':[5]
        },
    }