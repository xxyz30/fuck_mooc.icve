import json
import math
from urllib import request as req

import Config

# 爬取所有的课程


# 获得所有课程
# 请求Url为https://mooc.icve.com.cn/portal/Major/moocSearch?searchString=&type=course&province=&page=1&pageSize=20
from Crawl import SQL
from Main.DoCourse import DoCourse


def getAllCourse(page):
    url = f"https://mooc.icve.com.cn/portal/Major/moocSearch?page={page}&type=course&pageSize=20"
    resp = req.urlopen(req.Request(url, headers=Config.getHeaders()))
    return json.loads(resp.read())


# 加入课程
# https://mooc.icve.com.cn/portal/Course/getMoocCourseDetail?courseId=KFZNB710704&courseOpenId=&courseType=0&isNewApi=true
# 课程信息

# https://mooc.icve.com.cn/portal/Course/getAllCourseClass?courseId=KFZNB710704&isNewApi=true
# 课程第几次开课
# 上面的没啥用
# 请求地址：https://mooc.icve.com.cn/study/Learn/addMyMoocCourse?courseOpenId=
# courseOpenId为课程ID
def joinCourse(courseOpenId):
    url = f"https://mooc.icve.com.cn/study/Learn/addMyMoocCourse?courseOpenId={courseOpenId}"
    resp = req.urlopen(req.Request(url, headers=Config.getHeaders()))
    return json.loads(resp.read())["code"] == 1


# https://mooc.icve.com.cn/study/workExam/detail?courseOpenId=4ljtabatvkjjmrkllppccg&workExamId=frttabatppj0bmt2qe7nq&workExamType=1
# 为获得作答记录，可以拿到 studentWorkId，即作答的ID
# courseOpenId为课程ID，workExamId为作答ID
def getstudentWorkId(courseOpenId, workExamId):
    url = f"https://mooc.icve.com.cn/study/workExam/detail?courseOpenId={courseOpenId}&workExamId={workExamId}"
    resp = req.urlopen(req.Request(url, headers=Config.getHeaders()))
    return json.loads(resp.read())


# https://mooc.icve.com.cn/study/workExam/history?courseOpenId=?&workExamId=?&studentWorkId=?
# 获得作答记录
def getAnsower(courseOpenId, workExamId):
    studentWorkId = getstudentWorkId(courseOpenId, workExamId)
    if len(studentWorkId["list"]) != 0:
        studentWorkId = studentWorkId["list"][0]["Id"]
        url = f"https://mooc.icve.com.cn/study/workExam/history?courseOpenId={courseOpenId}&workExamId={workExamId}&studentWorkId={studentWorkId}"
        resp = req.urlopen(req.Request(url, headers=Config.getHeaders()))
        return json.loads(resp.read())
    else:
        print(f"课程{courseOpenId}的{workExamId}试题没有任何答题记录，爬取错误！")


def crawlCourse(courses):
    for x in courses:
        courseOpenId = x["courseOpenId"]
        if not joinCourse(courseOpenId):
            continue
        # 做题，做全部错误的题，再拿正确答案
        do = DoCourse(courseOpenId, True)
        do.run()
        # 再拿到所有的列表
        for i in do.examType:
            do.workExamType = i
            exams = do.getExamList(1)["list"]
            for j in exams:
                # stuWorkExamId = j["stuWorkExamId"]
                workExamId = j["Id"]
                answerList = getAnsower(courseOpenId, workExamId)
                resList = do.getTrueAnswerList(answerList, True)
                # 存储数据库
                SQL.insert(resList)


def run(startPage=1):
    # 先分页查找
    nowPage = startPage
    while True:
        allCourse = getAllCourse(nowPage)
        try:
            crawlCourse(allCourse["list"])
        except Exception as ex:
            print(f"出现异常了。目前爬取到了{nowPage}页")
            raise ex

        pagination = allCourse["pagination"]
        allPage = math.ceil(pagination["totalCount"] / pagination["pageSize"])

        if nowPage >= allPage:
            break
        nowPage += 1
