import requests
import json
import time
from PIL import Image
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}


def login():
    codeUrl = "https://mooc.icve.com.cn/portal/LoginMooc/getVerifyCode?ts={}".format(int(round(time.time() * 1000)))
    loginUrl = "https://mooc.icve.com.cn/portal/LoginMooc/loginSystem"
    codeResult = requests.post(url=codeUrl, headers=headers)
    with open("verifycode.jpg", "wb", ) as f:
        f.write(codeResult.content)
    code_cookies = codeResult.cookies
    img = Image.open("verifycode.jpg")
    img.show()
    name = input("请输入用户名:")
    password = input("请输入密码:")
    data = {
        'userName': name,
        'password': password,
        'verifycode': input("请输入验证码：")
    }
    result = requests.post(url=loginUrl, data=data, headers=headers, cookies=code_cookies)
    json_result = json.loads(result.text)
    if json_result['code'] == 1 and json_result['msg'] == "登录成功":
        Cookies = {
            "token": json_result['token'],
            "auth": result.cookies.get('auth'),
            "acw_tc": code_cookies.get('acw_tc'),
            "verifycode": code_cookies.get('verifycode')
        }
        return Cookies
    else:
        print(json_result['msg'])
        return 0


def get_cookies():
    cookies = login()
    return cookies
