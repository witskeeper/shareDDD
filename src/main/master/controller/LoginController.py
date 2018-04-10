# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.service.impl.LoginServiceImpl import LoginService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('LoginController')
logger.write_to_file(SystemConfig.logPathPrefix+"LoginController.log")

class LoginHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                # lambda alias
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @run_on_executor
    def execute_post(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'get_current_user' : lambda : self.get_current_user(),
                'auth_login' : lambda : self.auth_login(),
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def get_current_user(self):
        userName = self.get_argument('userName')
        userId=self.get_secure_cookie(userName)
        if not userId:
            return None
        return

    def any_author_exists(self):
        return bool

    def auth_login(self):
        data = json.loads(self.request.body)
        dataResult = LoginService().getUserInfo(data)
        if  dataResult.getMessage()[0]["username"] is None:
            return
        logger.error(data["passWord"])
        logger.error(type(data["passWord"]))
        if data["passWord"] == dataResult.getMessage()[0]["passwd"]:
            self.set_secure_cookie("userName", str(dataResult.getMessage()[0]["username"]),version=1)
            self.set_secure_cookie("userId", str(dataResult.getMessage()[0]["id"]), version=1)
        else:
            return "密码错误"
        return

    def auth_logout(self):
        data = json.loads(self.request.body)
        self.clear_cookie(data["userName"])
        return