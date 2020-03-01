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
		CREATE TABLE IF NOT EXISTS {table***REMOVED***(

		id INT NOT NULL,
		name VARCHAR(50) NOT NULL,
		address VARCHAR(100),
		latitude VARCHAR(20),
		longitude VARCHAR(20),
		phone VARCHAR(50),

		city_id INT NOT NULL,

		PRIMARY KEY(id),
		FOREIGN KEY (city_id)
		REFERENCES {city_table***REMOVED***(id)
	)
	""".format(table='{table***REMOVED***', city_table=settings.CITY_TABLE)

	def spider_generator(self, city_id, from_page=1, is_original=False):
		"""
		指定城市的店铺列表 生成器
		爬取地址：https://www.meituan.com/{keyword***REMOVED***/
		Args:
			city_id: 城市id，int
			from_page: 查询起始页码，int
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			shop_data: 一条商铺信息记录，list
		"""

		while True:
			print('城市id', str(city_id), '正在爬取商铺列表第', str(from_page), '页......')
			
			# 设置页码
			self.params['offset'] = str((from_page - 1) * int(self.params['limit']))
			
			# 更新cookies
			self.change_cookies(city_id)

			# 爬取一页商铺列表
			req = self.get(settings.MEI_TUAN_API_URL + str(city_id), self.params)
			
			# 判断IP是否被封
			if req.status_code in [403, 405]:
				print('城市id', str(city_id), '爬取商铺列表第', str(from_page), '页失败：', '爬虫被识别，请更换IP或Cookie')
				raise
			
			req_json = req.json()
			shop_list = req_json['data']['searchResult']

			# 如果商铺列表返回为空，则退出循环
			if not shop_list:
				print('城市id', city_id, '的所有商铺已经爬取完成！')
				break

			# 休息一下
			sleep(settings.SLEEP_TIME)

			for shop in shop_list:
				# 直接返回美团原生的商铺信息
				if is_original:
					yield shop
				***REMOVED***
					# 返回经过过滤的商铺信息
					shop_filter = {
						'id': shop['id'],
						'name': shop['title'],
						'address': shop['address'],
						'latitude': shop['latitude'],
						'longitude': shop['longitude'],
						'phone': shop['phone'],
						'city_id': city_id,
				***REMOVED***
					yield shop_filter
			from_page += 1

	def spider(self, city_id, from_page=1, is_original=False):
		"""
		爬取店铺信息
		Args:
			city_id: 城市id，int
			from_page: 查询起始页码，int
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			shop_filter: 店铺信息的查询记录，dict
		"""
		for shop in self.spider_generator(city_id, from_page, is_original):
			if self.name in shop.get('name', ''):
				print('商铺信息查询结果：')
				pprint(shop)
				return shop
		return '查无此店铺！'

if __name__ == '__main__':

	city = City('厦门')
	data = city.spider()
	city_id = data['id']

	shop = Shop('久匠纹眉旗舰店')

	# 指定的城市id中查询商铺信息
	# shop_info = shop.spider(city_id)
	# shop_info = shop.spider(city_id, is_original=True)

	# 更新数据库中所有商铺信息
	# city.mysql_update_all_from_spider()
	# shop.mysql_update_all_from_spider(city_id)
	shop.mysql_update_all_from_spider(city_id, from_page=31)
