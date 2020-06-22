from requests.adapters import HTTPAdapter
import requests
from urllib.parse import quote
from random import randrange
from pprint import pprint
import json

# 引入配置
import settings

# 禁用安全请求警告
try:
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except:
	pass

class Request(object):
	"""
	请求类
	"""
	if settings.PROXIES:
		proxy = settings.REQUESTS_PROXIES
	cookies = settings.REQUESTS_COOKIES
	params = settings.REQUESTS_PARAMS
	keyword = 'jiankangliren'

	def __init__(self, name='jiankangliren'):
		"""
		初始化
		Args:
			name: 请求关键字，str
		"""

		self.name = name

		# 更新cookies，城市默认62厦门
		self.change_cookies(62)

	def get(self, url, params=None):
		"""
		向网址发送get请求
		Args:
			url: 发送get请求的地址，str
			cookies: 设置请求Cookie，dict
			params: 设置请求参数，dict
		Returns:
			req: 返回响应对象，obj
		"""

		req_session = requests.Session()
		# 设置请求尝试连接次数最大值
		req_session.mount('http://', HTTPAdapter(max_retries=settings.MAX_RETRIES))
		req_session.mount('https://', HTTPAdapter(max_retries=settings.MAX_RETRIES))
		
		# 向网址发送get请求
		if settings.PROXIES:
			req = req_session.get(
									url,
									params=params,
									cookies=self.cookies,
									headers=settings.REQUESTS_HEADERS,
									timeout=settings.REQUESTS_TIMEOUT,
									proxies=settings.REQUESTS_PROXIES,
									verify=settings.REQUESTS_VERIFY,
								)
		else:
			req = req_session.get(
									url,
									cookies=self.cookies,
									params=params,
									headers=settings.REQUESTS_HEADERS,
									timeout=settings.REQUESTS_TIMEOUT,
									verify=settings.REQUESTS_VERIFY,
								)
		return req
	
	def change_cookies(self, city_id):
		"""
			变更cookies
		Args:
			city_id: 要查询的城市编号，int
		"""

		# 使用splash服务，更新cookies值
		if settings.SPLASH:
			lua = """
				function main(splash, args)
				  splash:go('"""+ settings.MEI_TUAN_DOMIN_URL + """')
				  splash:go('"""+ settings.MEI_TUAN_DOMIN_URL + """')
				  return splash:get_cookies()
				end
			"""
			if settings.PROXIES:
				url = '{splash}/execute?lua_source={lua}&proxy={proxy}'.format(
																			splash=settings.SPLASH_URL,
																			lua=quote(lua),
																			proxy=settings.REQUESTS_PROXIES['http']
																		)
			else:
				url = '{splash}/execute?lua_source={lua}'.format(
																splash=settings.SPLASH_URL,
																lua=quote(lua)
															)
			req_session = requests.Session()
			# 设置请求尝试连接次数最大值
			req_session.mount('http://', HTTPAdapter(max_retries=settings.MAX_RETRIES))
			req_session.mount('https://', HTTPAdapter(max_retries=settings.MAX_RETRIES))

			i = 0
			while True:
				try:
					req = req_session.get(url)
					cookies_json = req.json()
					for cookie in cookies_json:
						self.cookies[cookie['name']] = cookie['value'].replace('NaN', '2')
					if i:
						print('尝试获取Cookies成功！')
					i = 0
					break
				except Exception as err:
					print('更新Cookies', req, '失败：', err)
					if i == settings.MAX_RETRIES:
						print('尝试', settings.MAX_RETRIES, '次更新Cookies', row, '均失败！')
						break
					i += 1
					print('正在尝试重新获取Cookies:', '尝试次数', i, '次')

			# 更新get参数uuid
			self.params['uuid'] = self.cookies['uuid']

		# 更新cookies里的城市编号
		self.cookies['ci'] = self.cookies['rvct'] = str(city_id)

		return self.cookies

if __name__ == '__main__':
	
	obj = Request()

	# 查看访问美团域名后返回的cookies值
	# req = obj.get(settings.MEI_TUAN_DOMIN_URL)
	# cookies = dict(req.cookies)
	# pprint(cookies)

	# 配置里的cookies值
	# cookies = settings.REQUESTS_COOKIES
	# pprint(cookies)

	# 查看变更后的cookies值
	cookies = obj.change_cookies(62)
	pprint(cookies)