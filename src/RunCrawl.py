import json

import Config
from Crawl.GetAnswer import run
from Login.DoLogin import login

Config.Cookies = login()
page = input("爬取的页数")
if page == "":
    run()
else:
    run(int(page))
