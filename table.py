import pymysql
from pymysql.cursors import DictCursor

# 引入配置
import settings

class Table(object):
	"""
	表类
	"""

	def spider_generator(self, *args, **kwargs):
		"""
		爬取数据生成器
		"""
		pass

	def spider(self):
		"""
		爬取一条数据
		"""
		pass

	def mysql_create_table(self):
		"""
		创建数据表
		Args:
			table: 表名
		"""
		db = pymysql.connect(**settings.MYSQL)
		cursor = db.cursor()
		# 取消数据库警告
		cursor._defer_warnings = True
		self.create_table_sql = self.create_table_sql.format(table=self.table)
		# 创建表
		try:
			cursor.execute(self.create_table_sql)
		except Exception as err:
			db.rollback()
			print(self.table, '表创建失败！', err)
			return False
		cursor.close()
		db.close()
		print(self.table, '表创建成功！')
		return True

	def mysql_update(self, data, table):
		"""
		数据库更新一条记录
		"""
		if not table:
			table = self.table
		db = pymysql.connect(**settings.MYSQL)
		cursor = db.cursor()
		# 更新数据
		keys = ', '.join(data.keys())
		values = ', '.join(['%s'] * len(data))
		sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
		update = ','.join([" {key} = %s".format(key=key) for key in data])
		sql += update
		try:
			cursor.execute(sql, tuple(data.values())*2)
			db.commit()
		except Exception as err:
			print('商铺详情更新数据失败：',err)
			return False
		cursor.close()
		db.close()
		print('商铺详情更新数据成功！')
		return True

	def mysql_update_from_spider(self, *args, **kwargs):
		"""
		爬取一条数据更新到数据表
		Returns:
			status: 是否导入成功，True：导入成功，False：导入失败，Bool
		"""
		row = self.spider(*args, **kwargs)
		if row:
			db = pymysql.connect(**settings.MYSQL)
			cursor = db.cursor()
			# 更新数据
			keys = ', '.join(row.keys())
			values = ', '.join(['%s'] * len(row))
			sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=self.table, keys=keys, values=values)
			update = ','.join([" {key} = %s".format(key=key) for key in row])
			sql += update
			try:
				cursor.execute(sql, tuple(row.values())*2)
				db.commit()
			except Exception as err:
				print(self.table, '导入数据失败：',err)
				return False
			cursor.close()
			db.close()
			print(self.table, '表导入数据成功！')
			return True
		return False

	def mysql_update_all_from_spider(self, *args, **kwargs):
		"""
		爬取所有数据更新到数据表
		Returns:
			status: 是否导入成功，True：导入成功，False：导入失败，Bool
		"""

		db = pymysql.connect(**settings.MYSQL)
		cursor = db.cursor()
		# 更新数据
		for data in self.spider_generator(*args, **kwargs):
			keys = ', '.join(data.keys())
			values = ', '.join(['%s'] * len(data))
			sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=self.table, keys=keys, values=values)
			update = ','.join([" {key} = %s".format(key=key) for key in data])
			sql += update
			try:
				cursor.execute(sql, tuple(data.values())*2)
				db.commit()
			except Exception as err:
				print(self.table, '导入数据失败：',err)
		cursor.close()
		db.close()
		print(self.table, '表导入数据成功！')
		return True

	def mysql_query_generator(self, start_id=1):
		"""
		数据表查询 生成器
		Returns:
			row: 返回一条数据库记录
		"""

		db = pymysql.connect(**settings.MYSQL)

		cursor = db.cursor(DictCursor)

		if start_id:
			sql = 'SELECT * FROM {table} WHERE id >= {start_id}'.format(table=self.table, start_id=start_id)
		else:
			sql = 'SELECT * FROM {table}'.format(table=self.table)

		# 查询表
		try:
			cursor.execute(sql)
			for row in cursor.fetchall():
				yield row
		except Exception as err:
			print(self.table, '表查询失败！', err)
			return False
		cursor.close()
		db.close()

	def mysql_query(self):
		"""
		数据库查询返回一条数据
		Returns:
			row: 返回一条数据库记录
		"""

		db = pymysql.connect(**settings.MYSQL)
		cursor = db.cursor(DictCursor)
		sql = 'SELECT * FROM {table} WHERE name LIKE "%{name}%"'.format(table=self.table, name=self.name)
		# 查数据表
		try:
			cursor.execute(sql)
			row = cursor.fetchone()
		except Exception as err:
			print(self.table, '表，关键字', self.name, '数据查询失败！', err)
			return False
		cursor.close()
		db.close()
		print(self.table, '表，关键字', self.name, '数据查询结果：', row)
		return row