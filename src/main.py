from Main.DoCourse import *
import Config
from Login.DoLogin import login
from Main.GetAllCourse import getAllCourse


Config.Cookies = login()
# 课程ID
# courseOpenId = input("courseOpenId:")
# 题库服务器
Config.BankServer = input("请输入题库服务器，输入错误的话可能会导致提交空题目上去:")
while True:
    autoCommit = input("是否自动提交？（输入t则是，f则否，默认为是）（文本则如果有非单选、多选、判断的题目，建议不要）")
    if autoCommit == 't' or autoCommit == "":
        Config.AutoCommit = True
        break
    elif autoCommit == 'f':
        Config.AutoCommit = False
        break


for i in getAllCourse()["list"]:
    courseOpenId = i["courseOpenId"]
    print(i["courseName"] + courseOpenId)
    DoCourse(courseOpenId).run()
