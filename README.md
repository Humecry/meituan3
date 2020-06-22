# 美团商铺爬虫3
## 爬虫部署
### 安装Python及其常用依赖库  
- Anaconda下载: [点击下载](https://www.anaconda.com/distribution/#download-section)  
请选择Python 3.7 version版本  

- Anaconda安装教程: [点击查看](https://blog.csdn.net/u012318074/article/details/77075209)  
安装步骤Advanced Options中两个选项都要勾选, 第一个是加入环境变量, 第二个是默认使用Python。

- 安装本项目依赖库
```
pip install -r requirements.txt
```

### 使用Docker启动Splash
- 安装Docker教程：[点击查看](https://yeasy.gitbooks.io/docker_practice/install/windows.html)
- 通过Docker安装Splash
```
docker pull scrapinghub/splash
```

- 开启splash服务
```
docker run --restart=always -p 8050:8050 scrapinghub/splash
```
只需运行一次即可，以后随docker一起启动。
splash是为了模拟运行js动态获取cookies值，如果不更新cookies值爬取一定数量后，链接会失效。

### 运行项目
```
python meituan3
```

## 项目说明

爬取美团商铺分三个阶段：

- 第一阶段：一次性爬取所有城市信息到city表

- 第二阶段：通过读取第一阶段保存在数据库中的城市三级域名，按城市id由小到大的顺序一页一页爬取所有城市的商铺列表，包括的信息有商铺id，name，address，latitude，longitude，pyhone，city_id。每爬取一条商铺信息就保存到shop表

- 第三阶段：通过读取第二阶段保存在数据库中的商铺id，按商铺id由小到大爬取商铺详情更新shop表所有商铺字段，并保存图片url到album表

主程序保存在`__main__.py`文件中，在第二阶段中，start_id为爬取起始城市id，在第三阶段中start_id为爬取起始商铺id。如果第一阶段爬取过了，可以注释掉不用再爬取。如果第一第二阶段爬取过了，也可以注释掉，直接开始第三阶段爬取。

数据库，代理等配置放在`settings.py`文件中

代理推荐用阿布云代理，动态版

## 数据字典
以下三个表格在数据库中不存在时，python代码会自动创建，不需要自己建表
-  `city` 城市信息表，储存城市信息

|字段|类型|是否为空|注释|
|:----    |:-------    |:--- |------      |
|id    |int(0)     |否  |   城市id主键，来自美团的城市编号         |
|name |varchar(20) |否   |   城市中文名称   |
|letter     |varchar(10) |否   |    城市拼音首字母，方便城市索引     |
|third_level_domin |int(50)     |否   |   城市的三级域名  |

数据来源：
https://www.meituan.com/changecity/


    
-  `shop` 商铺信息表，储存商铺信息

|字段|类型|是否为空|注释|
|:----    |:-------    |:--- |------      |
|id    |int(0)     |否 |  商铺id主键，来自美团的商铺编号         |
|first_category  |varchar(20) |是   |     一级目录   |
|second_category |varchar(20) |是   |     二级目录   |
|third_category |varchar(20) |是   |    三级目录   |
|name |varchar(20) |否   |    商铺中文名称   |
|address |varchar(50) |是   |    商铺地址   |
|latitude |varchar(20) |是   |    纬度   |
|longitude |varchar(20) |是   |    经度   |
|phone |varchar(50) |是   |    商铺电话   |
|open_time |varchar(100) |是   |    营业时间   |
|wifi |tinyint(0) |是   |    是否有wifi，0: 没有，1: 有   |
|park |varchar(10) |是   |    是否有停车位，有：停车位，没有：None   |
|city_id    |int(0)     |否 |  关联城市id外键        |

数据来源：
https://{third_level_domin}/jiankangliren/pn{page}/
https://{third_level_domin}/jiankangliren/{shop_id}/


    
-  `album` 图片表，储存商铺图片

|字段|类型|空|注释|
|:----    |:-------    |:--- |------      |
|url |varchar(200) |否 |    商铺图片URL地址，为主键  |
|shop_id    |int(0)     |否 |  关联商铺id外键        |

数据来源：
https://www.meituan.com/jiankangliren/{shop_id}/