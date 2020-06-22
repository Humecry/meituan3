from lxml import etree
from pprint import pprint
import json
import pymysql
from time import sleep

# 引入公共类
from request import Request
from table import Table
# 引入城市类
from __1__city import City
# 引入配置
import settings

class Shop(Request, Table):

	"""
	店铺类
	"""

	# 店铺表名
	table = settings.SHOP_TABLE

	# 创建店铺表的SQL语句
	create_table_sql = """
		CREATE TABLE IF NOT EXISTS {table}(

		id INT NOT NULL,
		first_category VARCHAR(20),
        second_category VARCHAR(20),
        third_category VARCHAR(20),
		name VARCHAR(50) NOT NULL,
		address VARCHAR(100),
		latitude VARCHAR(20),
		longitude VARCHAR(20),
		phone VARCHAR(50),
		open_time VARCHAR(100),
        wifi TINYINT,
        park VARCHAR(10),

		city_id INT NOT NULL,

		PRIMARY KEY(id),
		FOREIGN KEY (city_id)
		REFERENCES {city_table}(id)
	)
	""".format(table='{table}', city_table=settings.CITY_TABLE)

	def spider_generator(self, city_data, from_page=1, is_original=False):
		"""
		指定城市的店铺列表 生成器
		爬取地址：https://www.meituan.com/{keyword}/
		Args:
			city_data: 城市数据，dict
			from_page: 查询起始页码，int
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			shop_data: 一条商铺信息记录，list
		"""

		while True:
			print('城市id', city_data['id'], '正在爬取商铺列表第', from_page, '页......')
			
			url = 'https://{third_level_domin}/{keyword}/pn{from_page}/'.format(
																				third_level_domin=city_data['third_level_domin'],
																				keyword=self.keyword,
																				from_page=from_page
																			)

			i = 0
			while True:
				try:
					req = self.get(url)

					# 判断IP是否被封
					if req.status_code in [403, 405]:
						print('城市id', city_data['id'], '爬取商铺列表第', from_page, '页失败：', '爬虫被识别，请更换IP或Cookie')

					root = etree.HTML(req.content)
					scripts = root.xpath('//*[@id="main"]/script[3]')
					json_string = scripts[0].text.replace('window.AppData = ', '').replace('}}};', '}}}')       
					req_json = json.loads(json_string)

					shop_list = req_json['searchResult']['searchResult']

					if i:
						print('尝试连接成功！已经爬取到数据！')
					i = 0
					break
				except Exception as err:
					print('城市id', city_data['id'], '商铺列表第', from_page, '页连接失败：', err)
					if i == settings.MAX_RETRIES:
						print('城市id', city_data['id'], '商铺列表第', from_page, '页尝试连接', settings.MAX_RETRIES, '次均失败！')
						break
					i += 1
					print('正在尝试重新连接:', '尝试次数', i, '次')
					# 更新cookies
					self.change_cookies(city_data['id'])

			# 如果商铺列表返回为空，则退出循环
			if not shop_list:
				print('城市id', city_data['id'], '的所有商铺已经爬取完成！')
				break

			# 休息一下
			sleep(settings.SLEEP_TIME)

			for shop in shop_list:
				# 直接返回美团原生的商铺信息
				if is_original:
					yield shop
				else:
					# 返回经过过滤的商铺信息
					shop_filter = {
						'id': shop['id'],
						'name': shop['title'],
						'address': shop['address'],
						'latitude': shop['latitude'],
						'longitude': shop['longitude'],
						'phone': shop['phone'],
						'city_id': city_data['id'],
					}
					yield shop_filter
			from_page += 1

	def spider(self, city_data, from_page=1, is_original=False):
		"""
		爬取一条店铺信息
		Args:
			city_data: 城市数据，dict
			from_page: 查询起始页码，int
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			shop_filter: 店铺信息的查询记录，dict
		"""

		for shop in self.spider_generator(city_data, from_page, is_original):
			if self.name in shop.get('name', '') or self.name in shop.get('title', ''):
				print('商铺信息查询结果：')
				pprint(shop)
				return shop
		return '查无此店铺！'

if __name__ == '__main__':

	city = City('厦门')
	city_data = city.spider()

	shop = Shop('米兰造型')

	# 爬取指定的城市的商铺信息
	# shop_info = shop.spider(city_data)

	# 爬取指定的城市的美团原生商铺信息
	# shop_info = shop.spider(city_data, is_original=True)

	# 创建数据表
	# shop.mysql_create_table()
	
	# 更新商铺一条数据
	# shop.mysql_update_from_spider(city_data)

	# 更新数据库中所有商铺信息
	# shop.mysql_update_all_from_spider(city_data)

	# 从数据库中查询店铺信息
	# shop.mysql_query()
