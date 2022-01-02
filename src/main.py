import json
import random
import time
from urllib import request as req

# 自动刷题
# 请求路径：https://mooc.icve.com.cn/study/workExam/workExamPreview
# get方法进行URL重写请求
_bl_uid = input("_bl_uid:")
verifycode = input("verifycode:")
auth = input("auth:")
token = input("token:")
TY_SESSION_ID = input("TY_SESSION_ID:")
acw_tc = input("acw_tc:")
workExamType = input("workExamType:")
# 课程ID
courseOpenId = "crrzaymtuypgrgynmrmfq"  # java的ID

# 不同的完成种类有不同的键值
typeKeyList = ["workExamData", "paperData"]

headers = {
    "Host": "mooc.icve.com.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": f"_bl_uid={_bl_uid}; verifycode={verifycode}; auth={auth}; token={token}; TY_SESSION_ID={TY_SESSION_ID}; acw_tc={acw_tc}",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "max-age=0",
}


# workExamId 为测试ID

# 获得本试卷的正确答案，返回字典
# {"题目ID": 答案}
def getTrueAnswerList(ansData):
    list = {}
    for x in typeKeyList:
        try:
            data = ansData[x]
            if workExamType == 2:
                datas = json.loads(data)
            else:
                datas = data
            questions = datas["questions"]
            for i in questions:
                try:
                    answerList = i["answerList"]
                    if len(answerList) == 0:
                        raise Exception()
                    for j in range(0, len(answerList)):
                        if answerList[j]["IsAnswer"] == 'True':
                            list[i["questionId"]] = j
                            # 暂时只有单选
                            continue
                    else:
                        continue
                except Exception as ex:
                    # print(ex)
                    print(i["TitleText"] + "\n可能是非单选题")
        except:
            pass
    return list


def request(workExamId):
    work = "https://mooc.icve.com.cn/study/workExam/workExamPreview"
    test = f"?courseOpenId={courseOpenId}&workExamId={workExamId}&agreeHomeWork=agree&workExamType={workExamType}"
    resp = req.urlopen(req.Request(work + test, headers=headers))
    return json.loads(resp.read())


# 暂存题目答案
# https://mooc.icve.com.cn/study/workExam/onlineHomeworkAnswer 为保存每个题目的答案,必须用Post
# 必填参数为： questionId=2tw1aj2osjlf0iinyzejfq&answer=1&questionType=1&uniqueId=..
# questionId为问题ID
# answer 为答案
# questionType为问题的种类，1应该是单选题
# uniqueId属于暂存ID，提交答案时要带上

def putAnswer(questionId, answer, uniqueId):
    print(questionId)
    url = "https://mooc.icve.com.cn/study/workExam/onlineHomeworkAnswer"
    params = f"?questionId={questionId}&answer={answer}&questionType=1&uniqueId={uniqueId}"

    resp = req.urlopen(req.Request(url + params, headers=headers, method="POST"))


# https://mooc.icve.com.cn/study/workExam/workExamSave
# uniqueId=uu1iaqoucl9prqnmllgl0q&workExamId=g7ttabatu49b7nptofvoq&workExamType=1&courseOpenId=4ljtabatvkjjmrkllppccg&paperStructUnique=&useTime=8
# uniqueId 为暂存区ID
# workExamId 为试卷ID
# workExamType 为试卷种类
# courseOpenId 为课程ID
# useTime 花费时间
def submitAnswer(uniqueId, workExamId):
    url = "https://mooc.icve.com.cn/study/workExam/workExamSave"
    params = f"?uniqueId={uniqueId}&workExamId={workExamId}&workExamType={workExamType}&courseOpenId={courseOpenId}&paperStructUnique=&useTime={random.randint(10, 40)}"
    resp = req.urlopen(req.Request(url + params, headers=headers, method="POST"))
    print(f"试题 {workExamId}: {json.loads(resp.read())['msg']}")


# IsDoExam为1时已做，为0为未作
# https://mooc.icve.com.cn/study/workExam/getWorkExamList 获得所有试题
# page=4&workExamType=1&courseOpenId=4ljtabatvkjjmrkllppccg&pageSize=5000
# page为页码数,workExamType 为是测试种类, courseOpenId为课程ID,pageSize为获取大小
def getExamList(page):
    url = "https://mooc.icve.com.cn/study/workExam/getWorkExamList"
    params = f"?page={page}&workExamType={workExamType}&courseOpenId={courseOpenId}&pageSize=5000"
    resp = req.urlopen(req.Request(url + params, headers=headers))
    # print(resp.read())
    return json.loads(resp.read())


def getExamNoDoList(page):
    l = []
    for i in getExamList(page)["list"]:
        if i["IsDoExam"] == 0:
            l.append(i["Id"])
    return l


def run():
    list = getExamNoDoList(1)
    for j in list:
        time.sleep(0.5)
        workExamId = j
        print(workExamId)
        jsonObj = request(workExamId)

        # 暂存唯一ID
        uniqueId = jsonObj["uniqueId"]
        trueList = getTrueAnswerList(jsonObj)
        for i in trueList.keys():
            putAnswer(i, trueList[i], uniqueId)

        submitAnswer(uniqueId, workExamId)


run()
