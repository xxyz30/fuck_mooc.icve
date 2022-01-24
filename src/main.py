from Main.DoCourse import *
import Config
from Login.DoLogin import login
from Main.GetAllCourse import getAllCourse


Config.Cookies = login()
# 课程ID
# courseOpenId = input("courseOpenId:")

for i in getAllCourse()["list"]:
    courseOpenId = i["courseOpenId"]
    print(i["courseName"] + courseOpenId)
    # DoCourse(courseOpenId).run()
