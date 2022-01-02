import json
from urllib import request as req

import Config

# 获得本账户所有的课程信息
# 请求网址为：https://mooc.icve.com.cn/portal/Course/getMyCourse?isFinished=0&page=1&pageSize=100000
# isFinished课程完成种类
# page等为简单的分页
url = "https://mooc.icve.com.cn/portal/Course/getMyCourse?isFinished=0&page=1&pageSize=100000"


def getAllCourse():
    resp = req.urlopen(req.Request(url, headers=Config.getHeaders(), method="GET"))
    return json.loads(resp.read())
