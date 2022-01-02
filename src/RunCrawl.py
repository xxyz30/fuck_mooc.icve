import json

import Config
from Crawl.GetAnswer import run

Config.Cookies = json.loads(input("cookie"))["请求 Cookie"]
run()
