# 智慧职教MOOC学院自动刷题
智慧职教MOOC学院自动刷题，自动考试基于python（暂未完成）

安装python3后先打开安装依赖库.bat，再打开运行.bat即可。

需要一个题库服务器来取题目

### 如何爬取题库：
安装mysql，并安装PyMySQL

`pip install PyMySQL`

在Crawl文件夹下面的SQL.py文件中配置你的SQL账号和密码还有sql

运行项目根目录下的mooc.sql，创建数据库。

然后运行服务器端，交互方式为GET

`http://host:port?id=xxx`

响应为JSON

```json
{
  "code": 1,
  "answer": "1,2",
  "message": ""
}
```
`code`为状态码，1则是正常。当非1时会出现message字段。

最后把服务器IP发给别人就是了。


本脚本使用GNU通用公共许可证开源，注意协议内容，禁止商业销售