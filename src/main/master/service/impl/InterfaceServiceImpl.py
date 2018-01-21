# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.InterfaceDao import InterfaceDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('InterfaceServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"InterfaceServiceImpl.log")

class InterfaceService(object):

    def __init__(self):
        self.interfaceDaoInterface = InterfaceDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addInterfaceItem(self,args):
        if "params" not in args:
            args.setdefault("params",None)
        if "failure_response" not in args:
            args.setdefault("failure_response",None)
        if "success_response" not in args:
            args.setdefault("success_response",None)
        if "response_type" not in args:
            args.setdefault("response_type",None)
        if "status" not in args:
            args.setdefault("status",None)
        if "remarks" not in args:
            args.setdefault("remarks",None)
        return self.interfaceDaoInterface.addInterfaceItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def getInterfaceInfoById(self,apiId):
        args={}
        args.setdefault("apiId",apiId)
        return self.interfaceDaoInterface.getInterfaceInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteInterfaceItem(self,args):
        return self.interfaceDaoInterface.deleteInterfaceItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateInterfaceItem(self,args):
        dataResult = self.interfaceDaoInterface.getInterfaceInfoById(args.get("apiId"))
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.interfaceDaoInterface.updateInterfaceItem(args)
        logger.error("apiId [{}] is invalid".format(args.get("apiId")))
        dataResult.setMessage("apiId [{}] is invalid".format(args.get("apiId")))
        return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def enableInterfaceItem(self,args):
        return self.interfaceDaoInterface.enableInterfaceItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def disableInterfaceItem(self,args):
        return self.interfaceDaoInterface.disableInterfaceItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def getInterfaceInfosByProject(self,projectId,groupId,offset=0,limit=10):
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("groupId", groupId)
        args.setdefault("offset", offset)
        args.setdefault("limit", limit)
        return self.interfaceDaoInterface.getInterfaceInfosByProject(args)

