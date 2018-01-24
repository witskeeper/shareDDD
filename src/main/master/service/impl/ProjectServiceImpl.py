# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.ProjectDao import ProjectDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ProjectServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"ProjectServiceImpl.log")

class ProjectService(object):

    def __init__(self):
        self.ProjectDaoInterface = ProjectDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addProject(self,args):
        return self.ProjectDaoInterface.addProject(args)

    @AdminDecoratorServer.execImplDecorator()
    def getProjectInfoByName(self,name):
        args={}
        args.setdefault("name",name)
        return self.ProjectDaoInterface.getProjectInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteProject(self,args):
        return self.ProjectDaoInterface.deleteProject(args)

    @AdminDecoratorServer.execImplDecorator()
    def getProjectInfoById(self,projectId):
        args={}
        args.setdefault("projectId",projectId)
        return self.ProjectDaoInterface.getProjectInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getProjectList(self):
        return self.ProjectDaoInterface.getProjectList()

