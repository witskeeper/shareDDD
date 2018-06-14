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
from src.main.master.service.impl.DatabaseServiceImpl import DatabaseService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('DatabaseController')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseController.log")

class DatabaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Origin,x-requested-with,Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self,APIName):
        # no body
        self.set_status(204)
        self.finish()

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'getDatabaseInfoById': lambda: self.getDatabaseInfoById(),
                'getDatabaseList':lambda :self.getDatabaseList(),
                'getTableGroupInfoById': lambda: self.getTableGroupInfoById(),
                'getTableGroupList': lambda: self.getTableGroupList(),
                'getTableGroupRelationList': lambda: self.getTableGroupRelationList(),
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
                'addDatabase' : lambda : self.addDatabase(),
                'deleteDatabase':lambda :self.deleteDatabase(),
                'editDatabase':lambda :self.editDatabase(),
                'addTableGroup': lambda: self.addTableGroup(),
                'deleteTableGroup': lambda: self.deleteTableGroup(),
                'editTableGroup': lambda: self.editTableGroup(),
                'addTableGroupRelation': lambda: self.addTableGroupRelation(),
                'deleteTableGroupRelation': lambda: self.deleteTableGroupRelation(),
                'updateTableGroupRelation': lambda: self.updateTableGroupRelation(),
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
    def addDatabase(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        return DatabaseService().addDatabase(data)

    def getDatabaseInfoById(self):
        databaseId= self.get_argument("id")
        return DatabaseService().getDatabaseInfoById(databaseId)

    def getDatabaseList(self):
        # todo 后面传了bu的Id
        businessUnit = self.get_argument("id")
        return DatabaseService().getDatabaseList(businessUnit)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteDatabase(self):
        return DatabaseService().deleteDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editDatabase(self):
        logger.info(self.request.body)
        return DatabaseService().editDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTableGroup(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        # 数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        return DatabaseService().addTableGroup(data)

    def getTableGroupInfoById(self):
        tableGroupId = self.get_argument("id")
        return DatabaseService().getTableGroupInfoById(tableGroupId)

    def getTableGroupList(self):
        DBId = self.get_argument("id")
        return DatabaseService().getTableGroupList(DBId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTableGroup(self):
        return DatabaseService().deleteTableGroup(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTableGroup(self):
        logger.info(self.request.body)
        return DatabaseService().editTableGroup(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTableGroupRelation(self):
        logger.info(self.request.body)
        return DatabaseService().addTableGroupRelation(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTableGroupRelation(self):
        relationId = self.get_argument("id")
        return DatabaseService().deleteTableGroupRelation(relationId)

    def getTableGroupRelationList(self):
        relationId = self.get_argument("id")
        return DatabaseService().getTableGroupRelationList(relationId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTableGroupRelation(self):
        logger.info(self.request.body)
        return DatabaseService().updateTableGroupRelation(json.loads(self.request.body))
