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
    def get(self):
        yield self.execute_get()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        yield self.execute_post()

    @run_on_executor
    def execute_get(self):
        dataResult = DataResult()
        try:
            task_name = self.get_argument('task_name')
            tasks = {
                'getProjectInfoByName' : lambda : self.getProjectInfoByName(),
                'getProjectList':lambda :self.getProjectList()
                # lambda alias
            }
            self.write(json.dumps(tasks[task_name]().__dict__,cls=CJsonEncoder))
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
    def execute_post(self):
        dataResult = DataResult()
        try:
            task_name = self.get_argument('task_name')
            tasks = {
                'addProject' : lambda : self.addProject(),
                'deleteProject':lambda :self.deleteProject(),
                'editProject':lambda:self.editProject()
            }
            self.write(json.dumps(tasks[task_name]().__dict__,cls=CJsonEncoder))
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
        name = self.get_argument('name')
        createuserid = self.get_argument('createuserid')
        version=self.get_argument('version')
        args={}
        #NOTICE
        args.setdefault("name",name)
        args.setdefault("createuserid",createuserid)
        args.setdefault("version",version)
        return ProjectService().addProject(args)

    def editProject(self):
        name = self.get_argument('name')
        edituserid = self.get_argument('edituserid')
        version = self.get_argument('version')
        projectid=self.get_argument('projectid')
        args = {}
        # NOTICE
        args.setdefault("name", name)
        args.setdefault("edituserid", edituserid)
        args.setdefault("version", version)
        args.setdefault("projectid",projectid)
        return ProjectService().addProject(args)

    def getProjectInfoByName(self):
        name= self.get_argument("name")
        return ProjectService().getProjectInfoByName(name)

    def deleteProject(self):
        projectid=self.get_argument("projectid")
        args={}
        args.setdefault("projectid",projectid)
        return ProjectService().deleteProject(args)

    def getProjectList(self):
        return ProjectService().getProjectList()