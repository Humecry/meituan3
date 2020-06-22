from __1__city import City
from __2__shop import Shop
from __3__album import Album
import settings

city = City()
shop = Shop()
album = Album()

# 阶段一：更新数据库城市表中数据
print('开始阶段一：更新城市表中数据')
city.mysql_create_table()
try:
	city.mysql_update_all_from_spider()
except Exception as err:
	print('更新数据库中的城市数据失败！', err)
print('更新城市表所有城市数据完成！')


# 阶段二：更新数据库商铺表中数据, start_id为爬取城市起始id
print('开始阶段二：更新商铺表中数据')
shop.mysql_create_table()
for row in city.mysql_query_generator(start_id=1):
	i = 0
	while True:
		try:
			shop.mysql_update_all_from_spider(row)
			if i:
				print('尝试更新成功！')
			i = 0
			break
		except Exception as err:
			print('更新城市', row, '的店铺数据失败：', err)
			if i == settings.MAX_RETRIES:
				print('尝试', settings.MAX_RETRIES, '次更新城市', row, '的店铺均失败！')
				break
			i += 1
			print('正在尝试重新更新城市', row, '的店铺数据:', '尝试次数', i, '次')
print('更新商铺表所有数据完成！')


# 阶段三：更新数据库商铺详情包括商铺图片表中数据
print('开始阶段三：更新商铺详情及图片表中数据')
album.mysql_create_table()
for row in shop.mysql_query_generator(start_id=1):
	i = 0
	while True:
		try:
			album.mysql_update_all_from_spider(row)
			if i:
				print('尝试更新成功！')
			i = 0
			break
		except Exception as err:
			print('更新商铺', row, '的图片数据失败：', err)
			if i == settings.MAX_RETRIES:
				print('尝试', settings.MAX_RETRIES, '次更新商铺', row, '的图片均失败！')
				break
			i += 1
			print('正在尝试重新更新商铺', row, '的图片数据:', '尝试次数', i, '次')
print('更新商铺详情及图片表中所有数据完成！')