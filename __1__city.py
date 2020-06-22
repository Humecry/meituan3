from lxml import etree
from pprint import pprint
import json
import pymysql

# 引入公共类
from request import Request
from table import Table
# 引入配置
import settings

class City(Request, Table):
	"""
	城市类
	"""

	# 城市表名
	table = settings.CITY_TABLE
	
	# 创建城市表的SQL语句
	create_table_sql = """
		CREATE TABLE IF NOT EXISTS {table}(

		id INT NOT NULL,
		name VARCHAR(20) NOT NULL,
		letter VARCHAR(10) NOT NULL,
		third_level_domin VARCHAR(30) NOT NULL,

		PRIMARY KEY(id)
	)
	"""

	def spider_generator(self, is_original=False):
		"""
		全国城市 生成器
		爬取地址：https://www.meituan.com/changecity/
		Args:
			name: 城市名称，str
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			city_filter: 返回一条城市记录
		"""

		url = settings.MEI_TUAN_DOMIN_URL + '/changecity/'
		req = self.get(url)
		root = etree.HTML(req.content)
		scripts = root.xpath('//*[@id="main"]/script[3]')
		json_string = scripts[0].text.replace('window.AppData = ', '').replace('}}};', '}}}')       
		data_json = json.loads(json_string)
		for data_list in data_json['openCityList']:
			for data in data_list[1]:
				# 直接返回美团原生的城市
				if is_original:
					yield data
				# 返回经过过滤的城市
				else:
					data_filter = {
						'id': data['id'],
						'name': data['name'],
						'letter': data['firstChar'],
						'third_level_domin': data['acronym'] + '.meituan.com',
					}
					yield data_filter

	def spider(self, is_original=False):
		"""
		查询一条城市数据
		Args:
			is_original: 是否返回美团原始数据，True：是，False：否，Bool
		Returns:
			row: 城市的查询记录，dict
		"""

		for row in self.spider_generator(is_original):
			if self.name in row.get('name', ''):
				print(self.name, '城市API查询结果：', row)
				return row
		print('查无此城市！')
		return False

if __name__ == '__main__':

	city = City('厦门')

	# 爬取经过筛选的城市
	data = city.spider()

	# 爬取美团原生的城市
	# city_original = city.spider(is_original=True)

	# 创建数据表
	# city.mysql_create_table()

	# 更新数据库中城市
	# city.mysql_update_from_spider()

	# 更新数据库中所有城市
	# city.mysql_update_all_from_spider()

	# 通过城市id查询数据库中城市
	# row = city.mysql_query()