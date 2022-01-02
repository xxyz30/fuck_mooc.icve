from Main.DoCourse import *
import json
import Config
from Main.GetAllCourse import getAllCourse

Config.Cookies = json.loads(input("cookie"))["请求 Cookie"]

# 课程ID
# courseOpenId = input("courseOpenId:")

for i in getAllCourse()["list"]:
    courseOpenId = i["courseOpenId"]
    print(i["courseName"] + courseOpenId)
    DoCourse(courseOpenId).run()
