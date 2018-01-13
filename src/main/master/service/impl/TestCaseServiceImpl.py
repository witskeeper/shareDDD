# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TestCaseDao import TestCaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestCaseServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseServiceImpl.log")

class TestCaseService(object):

    def __init__(self):
        self.testCaseDaoInterface = TestCaseDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTestCase(self,args):
        if "status" not in args:
            args.setdefault("status",None)
        if "remarks" not in args:
            args.setdefault("remarks",None)
        return self.testCaseDaoInterface.addTestCase(args)

    @AdminDecoratorServer.execImplDecorator()
    def getCaseInfosByCondition(self,projectId,groupId,offset=0,limit=10):
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("groupId", groupId)
        args.setdefault("offset", offset)
        args.setdefault("limit", limit)
        return self.testCaseDaoInterface.getCaseInfosByCondition(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestCase(self,args):
        return self.testCaseDaoInterface.deleteTestCase(args)

    @AdminDecoratorServer.execImplDecorator()
    def getCaseInfosById(self,caseId):
        args={}
        args.setdefault("caseId",caseId)
        return self.testCaseDaoInterface.getCaseInfosById(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTestCase(self,args):
        dataResult = self.testCaseDaoInterface.getCaseInfosById(args.get("caseId"))
        if dataResult.getSuccess() and len(dataResult.getMessage())>0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.testCaseDaoInterface.updateTestCase(args)
        logger.error("caseId [{}] is invalid".format(args.get("caseId")))
        dataResult.setMessage("caseId [{}] is invalid".format(args.get("caseId")))
        return dataResult
