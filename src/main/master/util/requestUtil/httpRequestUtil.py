# -*- coding: utf-8 -*-

import sys
import requests
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.entity.DataResult import DataResult

#set log
logger = Log('requestUtil')
logger.write_to_file(SystemConfig.logPathPrefix +"requestUtil.log")

class RequestBase(object):

    def __init__(self,url,method,format,params,timeout):
        self.url =url
        self.method = method
        self.format = format
        self.params = params
        self.timeout = timeout
        self.dataResult = DataResult()

    @AdminDecoratorServer.execImplDecorator()
    def getRequestInstance(self):
        return requests.Session()

    @AdminDecoratorServer.execImplDecorator()
    def parseDomain(self):
        self.dataResult.setSuccess(True)
        self.dataResult.setMessage(self.url.replace("http://","").split("/")[0])
        return self.dataResult

    @AdminDecoratorServer.execImplDecorator()
    def get(self):
        pass

    @AdminDecoratorServer.execImplDecorator()
    def post(self):
        pass
