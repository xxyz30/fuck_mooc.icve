import json
import random
import time
from urllib import request as req
from Config import *


# 自动刷题
# 请求路径：https://mooc.icve.com.cn/study/workExam/workExamPreview
# get方法进行URL重写请求
class DoCourse:
    # 不同的完成种类有不同的键值
    typeKeyList = ["workExamData", "paperData"]
    questionType = [1, 2, 3]
    examType = [0, 1, 2]

    def __init__(self, courseOpenId, crawlMode=False):
        # 课程ID
        self.courseOpenId = courseOpenId  # java的ID
        self.workExamType = 1
        self.crawlMode = crawlMode
        self.headers = getHeaders()

    # 获得本试卷的正确答案，返回字典
    # {"题目ID": 答案}
    # historyMode是在爬的时候用的
    def getTrueAnswerList(self, ansData, historyMode=False):
        list = {}
        for x in self.typeKeyList:
            try:
                data = ansData[x]
                if isinstance(data, str):
                    if data == '':
                        continue
                    datas = json.loads(data)
                else:
                    datas = data
                questions = datas["questions"]
                for i in questions:
                    if i["questionType"] in self.questionType:

                        if self.crawlMode:
                            if historyMode:
                                # 爬取模式且是历史模式时
                                # questionType = i["questionType"]
                                list[i["questionId"]] = i["Answer"]
                        else:
                            pass
                            # TODO 到时候请求题库服务器
                    else:
                        print(i["Title"] + "\n可能不是单选、多选或者判断")
            except Exception as ex:
                pass
                # print(ex)
        return list

    def request(self, workExamId):
        work = "https://mooc.icve.com.cn/study/workExam/workExamPreview"
        test = f"?courseOpenId={self.courseOpenId}&workExamId={workExamId}&agreeHomeWork=agree&workExamType={self.workExamType}"
        resp = req.urlopen(req.Request(work + test, headers=self.headers))
        return json.loads(resp.read())

    # 暂存题目答案
    # https://mooc.icve.com.cn/study/workExam/onlineHomeworkAnswer 为保存每个题目的答案,必须用Post
    # 必填参数为： questionId=2tw1aj2osjlf0iinyzejfq&answer=1&questionType=1&uniqueId=..
    # questionId为问题ID
    # answer 为答案,单选是数字，多选为：0,1，每个答案以,分割
    # questionType为问题的种类，1应该是单选题， 2是多选， 3是判断
    # uniqueId属于暂存ID，提交答案时要带上

    def putAnswer(self, questionId, answer, uniqueId):
        # 爬取模式则不需要提交答案
        if self.crawlMode:
            return
        # print(questionId)
        url = "https://mooc.icve.com.cn/study/workExam/onlineHomeworkAnswer"
        params = f"?questionId={questionId}&answer={answer}&questionType=1&uniqueId={uniqueId}"

        resp = req.urlopen(req.Request(url + params, headers=self.headers, method="POST"))

    # https://mooc.icve.com.cn/study/workExam/workExamSave
    # uniqueId=uu1iaqoucl9prqnmllgl0q&workExamId=g7ttabatu49b7nptofvoq&workExamType=1&courseOpenId=4ljtabatvkjjmrkllppccg&paperStructUnique=&useTime=8
    # uniqueId 为暂存区ID
    # workExamId 为试卷ID
    # workExamType 为试卷种类
    # courseOpenId 为课程ID
    # useTime 花费时间
    # 考试的URL提交：https://mooc.icve.com.cn/study/workExam/onlineExamSave
    # 参数和上面的一样，除了 workExamId 变成了 examId
    def submitAnswer(self, uniqueId, workExamId):
        if self.workExamType == 2:
            url = "https://mooc.icve.com.cn/study/workExam/onlineExamSave"
            examName = "examId"
        else:
            url = "https://mooc.icve.com.cn/study/workExam/workExamSave"
            examName = "workExamId"

        params = f"?uniqueId={uniqueId}&{examName}={workExamId}&workExamType={self.workExamType}&courseOpenId={self.courseOpenId}&paperStructUnique=&useTime={random.randint(10, 40)}"
        resp = req.urlopen(req.Request(url + params, headers=self.headers, method="POST"))
        print(f"试题 {workExamId}: {json.loads(resp.read())['msg']}")

    # IsDoExam为1时已做，为0为未作
    # https://mooc.icve.com.cn/study/workExam/getWorkExamList 获得所有试题
    # page=4&workExamType=1&courseOpenId=4ljtabatvkjjmrkllppccg&pageSize=5000
    # page为页码数,workExamType 为是测试种类, courseOpenId为课程ID,pageSize为获取大小
    def getExamList(self, page):
        url = "https://mooc.icve.com.cn/study/workExam/getWorkExamList"
        params = f"?page={page}&workExamType={self.workExamType}&courseOpenId={self.courseOpenId}&pageSize=5000"
        resp = req.urlopen(req.Request(url + params, headers=self.headers))
        return json.loads(resp.read())

    def getExamNoDoList(self, page):
        l = []
        for i in self.getExamList(page)["list"]:
            if i["IsDoExam"] == 0:
                l.append(i["Id"])
        return l

    def run(self):
        for x in self.examType:
            self.workExamType = x
            list = self.getExamNoDoList(1)
            print(f"没做的题{len(list)}")
            for j in list:
                time.sleep(0.5)
                workExamId = j
                # print(workExamId)
                jsonObj = self.request(workExamId)
                # 暂存唯一ID
                uniqueId = jsonObj["uniqueId"]
                if not self.crawlMode:
                    # 不是爬取模式时则不用暂存答案
                    trueList = self.getTrueAnswerList(jsonObj)
                    for i in trueList.keys():
                        self.putAnswer(i, trueList[i], uniqueId)

                self.submitAnswer(uniqueId, workExamId)
