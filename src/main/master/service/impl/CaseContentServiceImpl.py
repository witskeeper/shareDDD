# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.CaseContentDao import CaseContentDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('CaseContentServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"CaseContentServiceImpl.log")

class CaseContentService(object):

    def __init__(self):
        self.caseContentDaoInterface = CaseContentDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addCaseContent(self,args):
        if "interfaceid" not in args:
            args.setdefault("interfaceid",None)
        if "method" not in args:
            args.setdefault("method",None)
        if "format" not in args:
            args.setdefault("format",None)
        if "request_params" not in args:
            args.setdefault("request_params",None)
        if "timeout" not in args:
            args.setdefault("timeout",None)
        if "type" not in args:
            args.setdefault("type",None)
        if "sqlcontent" not in args:
            args.setdefault("sqlcontent", None)
        return self.caseContentDaoInterface.addCaseContent(args)

    @AdminDecoratorServer.execImplDecorator()
    def getContentInfosByCaseId(self,caseId):
        args={}
        args.setdefault("caseId",caseId)
        return self.caseContentDaoInterface.getContentInfosByCaseId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestContent(self,args):
        return self.caseContentDaoInterface.deleteTestContent(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestContentByCaseId(self,args):
        return self.caseContentDaoInterface.deleteTestContentByCaseId(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTestContent(self,args):
        dataResult =self.caseContentDaoInterface.getContentInfosByContentId(args.get("contentId"))
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key, value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key, value)
            return self.caseContentDaoInterface.updateTestContent(args)
        logger.error("contentId [{}] is invalid".format(args.get("contentId")))
        dataResult.setMessage("contentId [{}] is invalid".format(args.get("contentId")))
        return dataResult
