# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.GroupDao import GroupDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('GroupServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"GroupServiceImpl.log")

class GroupService(object):

    def __init__(self):
        self.GroupDaoInterface = GroupDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addGroup(self,args):
        if "type" not in args:
            args.setdefault("type",0)
        logger.error("args={0}".format(args))
        dataResult = self.GroupDaoInterface.getGroupInfoByName(args)
        logger.error("dataResult={0}".format(dataResult.getMessage()))
        if dataResult.getSuccess() and len(dataResult.getMessage()) == 0:
            return self.GroupDaoInterface.addGroup(args)
        dataResult.setMessage("group name [{0}] is exist,please retry other name".format(args.get("name")))
        dataResult.setSuccess(False)
        return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def getGroupInfoByProjectId(self,projectId,type=0):
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("type", type)
        return self.GroupDaoInterface.getGroupInfoByProjectId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteGroup(self,args):
        return self.GroupDaoInterface.deleteGroup(args)

