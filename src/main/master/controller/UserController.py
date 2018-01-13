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
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder

#set log
logger = Log('UserController')
logger.write_to_file(SystemConfig.logPathPrefix+"UserController.log")

class UserHandler(tornado.web.RequestHandler):
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
                'get_user_info_by_user_name' : lambda : self.get_user_info_by_user_name()
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
                'add_user_info' : lambda : self.add_user_info(),
                'delete_user_info':lambda :self.delete_user_info()
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

    def get_user_info_by_user_name(self):
        userName = self.get_argument('userName')
        return UserService().getUserInfo(userName)

    def add_user_info(self):
        dataResult = DataResult()
        data = json.loads(self.request.body)
        if 'userName' not in data:
            dataResult.setSuccess(False);
            dataResult.setMessage("Request Params[userName] must be provided")
            return dataResult
        if 'phone' not in data:
            dataResult.setSuccess(False);
            dataResult.setMessage("Request Params[phone] must be provided")
            return dataResult
        if 'sex' not in data:
            sex ="male"
        else:
            sex = data.get("sex")
        args={}
        #NOTICE
        args.setdefault("user_name",data.get("userName"))
        args.setdefault("user_phone",data.get("phone"))
        args.setdefault("user_sex",sex)
        return UserService().addUser(args)

    def delete_user_info(self):
        data = json.loads(self.request.body)
        return UserService().deleteUser(data["userName"])
