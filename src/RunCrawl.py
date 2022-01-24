import json

import Config
from Crawl.GetAnswer import run
from Login.DoLogin import login

Config.Cookies = login()
run()
