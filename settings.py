# 是否启用splash服务更新cookie的值。启用则需要安装splash插件
SPLASH = True
SPLASH_URL = 'http://localhost:8050'

# 是否启用Charles代理用于测试
CHARLES = False

# 是否启用第三方代理，启用后请设置REQUESTS_PROXIES值
PROXIES = True

# 设置第三方代理接口
if PROXIES:
	# 阿布云代理服务器
	proxy_host = 'http-dyn.abuyun.com'
	proxy_port = '9020'
	 
	# 代理隧道验证信息
	proxy_user = 'UF71V2703299U37D'
	proxy_pass = '109SB83DA4F47B98'
	
	proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
	    'host': proxy_host,
	    'port': proxy_port,
	    'user': proxy_user,
	    'pass': proxy_pass,
	}

	REQUESTS_PROXIES = {
	    'http': proxy_meta,
	    'https': proxy_meta,
	}

	# REQUESTS_PROXIES = {
	#   "http": "http://127.0.0.1:8887",
	#   "https": "http://127.0.0.1:8887",
	# }

	# REQUESTS_PROXIES = {
	#   "http": "http://127.0.0.1:1087",
	#   "https": "http://127.0.0.1:1087",
	# }

# 设置爬取等待时间，默认0秒
SLEEP_TIME = 0

# 设置请求超时等待时间，默认5秒
REQUESTS_TIMEOUT = 5

# 设置尝试次数，默认3次
MAX_RETRIES = 3

# 数据表名
CITY_TABLE = 'city'
SHOP_TABLE = 'shop'
ALBUM_TABLE = 'album'

# MySQL数据库配置
# MYSQL = {
# 	'host': 'localhost',
# 	'user': 'root',
# 	'password': 'root1234',
# 	'database': 'meituan',
# }
MYSQL = {
	'host': 'localhost',
	'user': 'root',
	'password': '1234',
	'database': 'just_for_test',
}

# 是否启用SSL安全验证
if CHARLES:
	# REQUESTS_VERIFY=True
	REQUESTS_VERIFY = '/Users/hume/Desktop/charles-ssl-proxying-certificate.pem'
	# REQUESTS_VERIFY = False
else:
	REQUESTS_VERIFY = False

# 美团域名
MEI_TUAN_DOMIN_URL = 'https://www.meituan.com'

# 设置请求头
REQUESTS_HEADERS = {
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
	'Sec-Fetch-Dest': 'document',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Sec-Fetch-Site': 'none',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-User': '?1',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh',
	'Referer': 'https://www.meituan.com/',
}

# 设置cookies
REQUESTS_COOKIES = {
	'__mta': '246797889.1582564028355.1582564028351.1582564028352.3',
	'uuid': 'd8b3fecb7f69475dae9f.1582535153.1.0.0',
	'ci': '62', # 城市编号
	'rvct': '62', # 城市编号
	'_lxsdk_cuid': '17066a155b0c8-0f056c63b1a0c5-396f7006-1fa400-17066a155b0c8', # 需要及时更新
	'_lxsdk_s': '170674ba5a2-baf-2d9-697%7C%7C8', # 需要及时更新
}

# 设置请求参数
REQUESTS_PARAMS = {
	'uuid': 'd8b3fecb7f69475dae9f.1582535153.1.0.0',
	'userid': '-1',
	'limit': '32',
	'offset': '32', # 代表页码数，第一页：32，第二页：64
	'cateId': '22',
	'areaId': '-1',
}

# 本地配置
try:
	from local_settings import *
except ImportError:
	pass