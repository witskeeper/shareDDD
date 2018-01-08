# -*- coding: utf-8 -*-

class SystemConfig:
    #后端日志存放路径,具体日志文件为logPathPrefix + 方法所在文件名称
    logPathPrefix="./LogFiles/"
    #后端http服务的端口,前端默认端口为8080
    httpPost=8090
    #钉钉通知webhook
    dingTalkWebHook=""

class DbConfig:
    #host="localhost"
    host="127.0.0.1"
    user="root"
    passwd="root"
    db="dba"
    port=3306