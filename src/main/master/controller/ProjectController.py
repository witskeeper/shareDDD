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
from src.main.master.service.impl.ProjectServiceImpl import ProjectService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder

#set log
logger = Log('ProjectController')
logger.write_to_file(SystemConfig.logPathPrefix+"ProjectController.log")

class ProjectHandler(tornado.web.RequestHandler):
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
                'getProjectInfoByName' : lambda : self.getProjectInfoByName(),
                'getProjectInfoById': lambda: self.getProjectInfoById(),
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
                'addProject' : lambda : self.addProject(),
                'deleteProject':lambda :self.deleteProject()
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

    def addProject(self):
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        if "remarks" not in  data:
            data.setdefault("remarks",None)
        if "version" not in  data:
            data.setdefault("version",None)
        return ProjectService().addProject(data)

    def getProjectInfoByName(self):
        name= self.get_argument("name")
        return ProjectService().getProjectInfoByName(name)

    def getProjectInfoById(self):
        name= self.get_argument("name")
        return ProjectService().getProjectInfoById(name)

    def deleteProject(self):
        return ProjectService().deleteProject(json.loads(self.request.body))