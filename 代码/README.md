# 你的个人生活终端

# 终端实现功能

## 代办事项

![todolist](..\photos\todolist.png)

由notion api开发的todolist。每个待办项都有名称、ddl（deadline）、star和importance level四个属性。

### 特点：

- 当ddl来临的那一天和以后，该代办项将变成反色来强调提醒。
- 拥有star作为一种强提示，star为与代办项底色相反的颜色，unstar为与代办项底色相同的颜色。star具体意义可以用户自定义，默认不填为unstar。
- 拥有importance level 作为重要度表示，1为最弱，5为最强，默认不填为1。

### 使用：

- 获取database_id
  - 建立notion账号
  - 创建一个库
  - 点击右上角三个点，点击copylink，保留link，后面有用
  - v=后面的就是该notion database的id
- 将database的properties设置为下图所示，其中：
  - 任务名称：type: Title；
  - DDL: type: Date; Date format: Full date; Time format: 12 hour
  - start date: type: Created time; Date format: Full date; Time format: 12 hour
  - star: type: Select; Options: star、unstar
  - importance: type: Select; Options: 5、4、3、2、1

<img src="D:\WorkingFiles\epd\photos\notion_properties.png" alt="notion_properties" style="zoom:50%;" />

- 获取个人API的令牌（Authorization）
  - [打开这个网页（My Integrations)](https://www.notion.so/my-integrations)
  - 点击【 + New Integration】
  - 维持原始设定，在name栏里随意填写你希望的名字
  - 点击提交
  - 复制内部集成令牌。它将以 secret_ 开头
  - 在你获得的key前面再添加上Bearer和一个空格
  - 你最终的令牌为“Bearer secret_”+一串字符
- 将获得的database_id填写到userConf.py的database_id=“”中
- 将获得的Authorization填写到userConf.py的Authorization=“”中
- 将database的link填写到index.html的herf=‘ ’中，可以搜索以下代码找到该语句

```html
<area class="picarea" shape="rect" coords="0,0,183,430" href=''>
```



## 天气

![weather](..\photos\weather.png)

由高德api通过ip地址获取城市信息，通过和风天气api获取该城市的具体实时天气。

### 特点：

- 美观设计
- 创新滑动条展示天气信息，一眼就明了
- 无需配置地理位置信息，可以动态获取（本地端）

### 使用：

- 获取高德API key：
  - [进入高德开放平台](https://lbs.amap.com/)
  - 注册或者登录开发者
  - [进入控制台](https://console.amap.com/dev/index)
  - 侧边栏-应用管理-我的应用-创建新应用
  - 填写名称类型（随意填写）然后点创建
  - 该条目下点添加
  - key名称随意，平台为web，然后提交
  - 将key栏下的字符复制下来，就是高德API的key
- 将获得的key填写到userConf.py的GaoDekey=“”中
- 获取和风天气API key：
  - [登录或注册和风天气](https://dev.qweather.com/docs/api/)
  - 侧边栏-应用管理-创建应用-免费开发版
  - 填写你的名称，选择web api
  - 填写key 名称
  - 将key栏下的字符复制下来，就是和风天气API的key

- 将获得的key填写到userConf.py的qweatherkey=“”中
- 如果你使用的是服务器端，你要再把自己的ip地址填写在userConf.py的userip = “”中，你的ip地址可以在[这个网站](http://mip.chinaz.com/)里查看（不是我的网站，仅仅是随意找的一个网页）

## 课程表、排班表

<img src="..\photos\classes.png" alt="classes" style="zoom:75%;" />

### 特点：

- 可以设置一学期的总周数、第一周的日期
- 一天分为5节课，上午下午各两节，晚上一节（大学课表）
- 根据导入的课表精准显示每天的课程

### 使用：

- 在userConf.py的classconf中的startmonday设置课程开始的周一的日期，格式为‘yyyy-mm-dd’,月数和日期小于10时请不要在前面加0。
- 在userConf.py的classconf中的weeks设置课程的周数，格式为‘number‘
- 在userConf.py的classlist设置课程，格式和介绍如下：

```python
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
}
```

## 多功能提示面板

<img src="..\photos\multyfunctional.png" alt="multyfunctional" style="zoom:50%;" />

### 特点：

- 平常情况下展示导入的图片，图片可以任意长宽比例，若为竖向图片有模糊化的背景填充
- 可以设定喝水的提醒实际，到达该时间后将会出现喝水提醒
- 可以设定他人的生日并在生日当天进行提醒，正常显示图片的情况下也在右下角有生日提醒。生日支持农历和太阳历。

### 使用：

- 希望可以展示的图片放在pic\photos中
- 喝水提醒的时间设置在userConf.py的water_drink_time，单位为分钟
- 生日的设置在userConf.py的birthday中，设置格式如下：

```python
{"name":"测试","calendar":"Chinese Calendar","month":7,"date":23},#calender:"Chinese Calendar"农历、"Solar Calendar"阳历
```

## 底栏

![under](..\photos\under.png)

展示当前联网情况、地理位置、阳历、农历、星期、时间

## 网页实现内容
