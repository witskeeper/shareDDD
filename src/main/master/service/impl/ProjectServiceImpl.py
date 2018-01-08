# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.ProjectDao import ProjectDaoInterface

#set log
logger = Log('ProjectServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"ProjectServiceImpl.log")

class ProjectService(object):

    def __init__(self):
        self.ProjectDaoInterface = ProjectDaoInterface()

    def addProject(self,args):
        dataResult = DataResult()
        try:
            if "name" in args:
                dataResult = self.ProjectDaoInterface.getProjectInfoByName(args)
                logger.info(dataResult.__dict__)
                if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
                    dataResult.setMessage("Ptoject name [{0}] is exists".format(args.get("name")))
                    dataResult.setSuccess(False)
                    return dataResult
                return self.ProjectDaoInterface.addProject(args)
            dataResult.setMessage("param name not suport")
            dataResult.setSuccess(False)
            return dataResult
        except Exception,e:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult

    def getProjectInfoByName(self,name):
        try:
            args={}
            args.setdefault("name",name)
            return self.ProjectDaoInterface.getProjectInfoByName(args)
        except Exception,e:
            dataResult = DataResult()
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult

    def deleteProject(self,args):
        try:
            return self.ProjectDaoInterface.deleteProject(args)
        except Exception, e:
            dataResult = DataResult()
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult

