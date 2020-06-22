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
from __2__shop import Shop
# 引入配置
import settings

class Album(Request, Table):

	"""
	店铺图片类
	"""

	# 图片表名
	table = settings.ALBUM_TABLE

	# 创建图片表的SQL语句
	create_table_sql = """
		CREATE TABLE IF NOT EXISTS {table}(

		url VARCHAR(300) NOT NULL,

		shop_id INT NOT NULL,

		PRIMARY KEY(url),
		FOREIGN KEY (shop_id)
		REFERENCES {shop_table}(id)
	)
	""".format(table='{table}', shop_table=settings.SHOP_TABLE)

	def spider_generator(self, shop_data, is_original=False):
		"""
		店铺图片 生成器
		爬取地址：https://www.meituan.com/{keyword}/{shop_id}/
		Args:
			shop_data: 一条商铺数据，dict
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			picture_filter: 商铺图片，dict
		"""

		print('商铺id', shop_data['id'], '正在爬取商铺详情与图片')

		i = 0
		while True:
			try:
				url = '{domin}/{keyword}/{shop_id}/'.format(
														domin=settings.MEI_TUAN_DOMIN_URL,
														keyword=self.keyword,
														shop_id=shop_data['id']
													)
				req = self.get(url)
				root = etree.HTML(req.content)
				scripts = root.xpath('//*[@id="main"]/script[3]')
				json_string = scripts[0].text.replace('window.AppData = ', '').replace('}}};', '}}}')       
				shop_json = json.loads(json_string)

				if shop_json.get('errorMsg') == '403':
						print('爬虫被识别，请更换IP或Cookie')

				poiInfo = shop_json['poiInfo']
				shop_album = shop_json['album']

				shop_info = {
					'id': poiInfo['id'],
					'first_category': poiInfo['cityName']+'美团',
					'second_category': poiInfo['cityName']+poiInfo['crumbs'][0]['title'],
					'third_category': poiInfo['cityName']+poiInfo['crumbs'][1]['title'],
					'name': poiInfo['name'],
					'address': poiInfo['address'],
					'latitude': poiInfo['lat'],
					'longitude': poiInfo['lng'],
					'phone': poiInfo['phone'],
					'open_time': poiInfo['openTime'],
					'wifi': poiInfo['wifi'],
					'park': poiInfo['park'],
					'city_id': shop_data['city_id'],
				}

				# 更新商铺详情数据
				self.mysql_update(shop_info, table=settings.SHOP_TABLE)

				if i:
					print('尝试连接成功！已经爬取到数据！')
				i = 0
				break

			except Exception as err:

				print('商铺id', shop_data['id'], '商铺详情页连接失败：', err)
				if i == settings.MAX_RETRIES:
					print('商铺id', shop_data['id'], '商铺详情页尝试连接', settings.MAX_RETRIES, '次均失败！')
					break
				i += 1
				print('正在尝试重新连接:', '尝试次数', i, '次')

				# 更新cookies
				self.change_cookies(shop_data['city_id'])

		# 休息一下
		sleep(settings.SLEEP_TIME)

		for picture in shop_album:
			# 直接返回美团原生的商铺图片
			if is_original:
				yield picture
			else:
				# 返回经过过滤的商铺图片
				picture_filter = {
					'url': picture['url'],
					'shop_id': shop_data['id'],
				}
				yield picture_filter

	def spider(self, shop_data, is_original=False):
		"""
		爬取一家商铺的所有图片
		Args:
			shop_data: 要爬取的商铺数据，dict
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			shop_filter: 返回一家商铺的所有图片，dict
		"""

		album = []
		for picture in self.spider_generator(shop_data, is_original):
			album.append(picture)
		print('商铺信息查询结果：')
		pprint(album)
		return album

if __name__ == '__main__':

	shop = Shop('米兰造型')

	shop_data = shop.mysql_query()

	album = Album()

	# 爬取指定的商铺的所有图片
	# album_info = album.spider(shop_data)

	# 爬取指定的商铺的美团原生所有图片
	# album_info = album.spider(shop_data, is_original=True)

	# 创建数据表
	# album.mysql_create_table()

	# 更新数据库中所有商铺信息
	# album.mysql_update_all_from_spider(shop_data)
