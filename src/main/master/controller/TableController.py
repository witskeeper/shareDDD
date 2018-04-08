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
from src.main.master.service.impl.TableServiceImpl import TableService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TableController')
logger.write_to_file(SystemConfig.logPathPrefix+"TableController.log")

class TableHandler(tornado.web.RequestHandler):
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
                'getTableInfoById': lambda: self.getTableInfoById(),
                'getTableList':lambda :self.getTableList(),
                'getColumnInfoById': lambda: self.getColumnInfoById(),
                'getColumnListByTableId': lambda: self.getColumnListByTableId(),
                'isInitSynchronize': lambda: self.isInitSynchronize(),
                'getDataRouteInfoById': lambda: self.getDataRouteInfoById(),
                'getDataRouteList': lambda: self.getDataRouteList(),
                'getDBLogList': lambda: self.getDBLogList(),
                'getLinkTableList': lambda: self.getLinkTableList(),
                'getLinkColumnList': lambda: self.getLinkColumnList(),
                'getTableRouteList': lambda: self.getTableRouteList(),
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
                'getTableInfoByName': lambda: self.getTableInfoByName(),
                'addTable' : lambda : self.addTable(),
                'deleteTable':lambda :self.deleteTable(),
                'editTable':lambda :self.editTable(),
                'editTableByName':lambda :self.editTableByName(),
                'discardTableByName':lambda :self.discardTableByName(),
                'getColumnListByTableName': lambda: self.getColumnListByTableName(),
                'addColumn': lambda: self.addColumn(),
                'deleteColumn': lambda: self.deleteColumn(),
                'editColumn': lambda: self.editColumn(),
                'initSynchronizeDatabase': lambda: self.initSynchronizeDatabase(),
                'synchronizeDatabase': lambda: self.synchronizeDatabase(),
                'initSynchronizeTable': lambda: self.initSynchronizeTable(),
                'initSynchronizeColumn': lambda: self.initSynchronizeColumn(),
                'editColumnRemarkById': lambda: self.editColumnRemarkById(),
                'editColumnDiscardById': lambda: self.editColumnDiscardById(),
                'getSearchByTable': lambda: self.getSearchByTable(),
                'getSearchByTableColumn': lambda: self.getSearchByTableColumn(),
                'getSearchByColumn': lambda: self.getSearchByColumn(),
                'addColumnLink': lambda: self.addColumnLink(),
                'getTableListByTableName': lambda: self.getTableListByTableName(),
                'getColumnListByColName': lambda: self.getColumnListByColName(),
                'addTableRoute': lambda: self.addTableRoute(),
                'addDataNode': lambda: self.addDataNode(),
                'addDataRoute': lambda: self.addDataRoute(),
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
    def addTable(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        return TableService().addTable(data)

    def getTableInfoById(self):
        TableId= self.get_argument("id")
        return TableService().getTableInfoById(TableId)

    def getTableInfoByName(self):
        data = json.loads(self.request.body)
        return TableService().getTableInfoByName(data)

    def getTableList(self):
        DBId = self.get_argument("id")
        return TableService().getTableList(DBId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTable(self):
        return TableService().deleteTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTable(self):
        logger.info(self.request.body)
        return TableService().editTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTableByName(self):
        logger.info(self.request.body)
        return TableService().editTableByName(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def discardTableByName(self):
        logger.info(self.request.body)
        return TableService().discardTableByName(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addColumn(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        return TableService().addColumn(data)

    def getColumnInfoById(self):
        columnId = self.get_argument("id")
        return TableService().getTableInfoById(columnId)

    def getColumnListByTableId(self):
        tableId = self.get_argument("id")
        return TableService().getColumnListByTableId(tableId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getColumnListByTableName(self):
        return TableService().getColumnListByTableName(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteColumn(self):
        return TableService().deleteColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnRemarkById(self):
        logger.info(self.request.body)
        return TableService().editColumnRemarkById(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnDiscardById(self):
        logger.info(self.request.body)
        return TableService().editColumnDiscardById(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumn(self):
        logger.info(self.request.body)
        return TableService().editColumn(json.loads(self.request.body))

    def isInitSynchronize(self):
        DBId = self.get_argument("id")
        return TableService().isInitSynchronize(DBId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeDatabase(self):
        logger.info(self.request.body)
        return TableService().initSynchronizeDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def synchronizeDatabase(self):
        logger.info(self.request.body)
        return TableService().synchronizeDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeTable(self):
        logger.info(self.request.body)
        return TableService().initSynchronizeTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeColumn(self):
        logger.info(self.request.body)
        return TableService().initSynchronizeColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByTable(self):
        logger.info(self.request.body)
        return TableService().getSearchByTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByTableColumn(self):
        logger.info(self.request.body)
        return TableService().getSearchByTableColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByColumn(self):
        logger.info(self.request.body)
        return TableService().getSearchByColumn(json.loads(self.request.body))

    def getDBLogList(self):
        DBId = self.get_argument("id")
        return TableService().getDBLogList(DBId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addColumnLink(self):
        data = json.loads(self.request.body)
        return TableService().addColumnLink(data)

    def getLinkTableList(self):
        DBId = self.get_argument("id")
        return TableService().getLinkTableList(DBId)

    def getLinkColumnList(self):
        tableId = self.get_argument("id")
        return TableService().getLinkColumnList(tableId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getTableListByTableName(self):
        data = json.loads(self.request.body)
        return TableService().getTableListByTableName(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getColumnListByColName(self):
        data = json.loads(self.request.body)
        return TableService().getColumnListByColName(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTableRoute(self):
        data = json.loads(self.request.body)
        return TableService().addTableRoute(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addDataNode(self):
        data = json.loads(self.request.body)
        return TableService().addDataNode(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addDataRoute(self):
        data = json.loads(self.request.body)
        return TableService().addDataRoute(data)

    def getTableRouteList(self):
        table_id = self.get_argument("id")
        return TableService().getTableRouteList(table_id)

