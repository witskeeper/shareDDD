# -*- coding: utf-8 -*-

import json
import traceback
import threadpool
import os
import time
import datetime
import socket
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TaskMetaqInfoDao import TaskMetaqInfoDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.dao.TestCaseInstanceDao import TestCaseInstanceDaoInterface
from src.main.master.dao.TestSuiteDao import TestSuiteDaoInterface

#set log
logger = Log('TaskCenterServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TaskCenterServiceImpl.log")

#global
pool = threadpool.ThreadPool(10)

class TaskCenterService(object):

    def __init__(self):
        pass

    @staticmehtod
    @AdminDecoratorServer.execImplDecorator()
    def __sendTaskJob(taskInfo):
        tmp_args={}
        tmp_args.setdefault("status","1")
        #hostname
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        tmp_args.setdefault("running_consumer","{0}|{1}".format(ip,hostname))
        tmp_args.setdefault("msg_id",os.getpid())
        tmp_args.setdefault("taskId",taskInfo.get("id"))
        dataResult = TaskMetaqInfoDaoInterface().updateTaskInfo(tmp_args)
        if dataResult.getSuccess():
            return TaskCenterService.__execTaskJob(taskInfo)
        else:
            tmp_args.setdefault("is_deleted",1)
            return TaskMetaqInfoDaoInterface().deleteTaskInfo(tmp_args)

    @staticmehtod
    @AdminDecoratorServer.execImplDecorator()
    def __execTaskJob(taskInfo):
        args = {}
        args.setdefault("instanceId", taskInfo.get("instanceid"))
        args.setdefault("build_start",datetime.datetime.now())
        result = DataResult()
        taskGlobalStatus = "Error"
        try:
            #set metaq db
            metaq_args={}
            metaq_args.setdefault("status", "2")
            #hostname
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            metaq_args.setdefault("running_consumer", "{0}|{1}".format(ip, hostname))
            metaq_args.setdefault("msg_id", os.getpid())
            metaq_args.setdefault("taskId", taskInfo.get("id"))
            TaskMetaqInfoDaoInterface().updateTaskInfo(metaq_args)
            dataResult = TestCaseInstanceDaoInterface().getTestInstanceInfoById(args)
            if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
                suiteId = dataResult.getMessage()[0].get("suite_id")
                status = dataResult.getMessage()[0].get("status")
                if status == "Waiting":
                    #set instance Running
                    args.setdefault("build_end", None)
                    args.setdefault("status", "Running")
                    TestCaseInstanceDaoInterface().updateTestInstance(args)
                    dataResult =TestSuiteDaoInterface().getSuiteInfoById({"suiteId":suiteId})
                    if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
                        caseIds = dataResult.getMessage()[0].get("testcaseids")
                        if caseIds is None:
                            caseIds = []
                        else:
                            caseIds = list(caseIds)
                        for caseId in caseIds:
                            dataResult =TestCaseInstanceDaoInterface().getTestInstanceInfoById(args)
                            if dataResult.getMessage()[0].get("status") not in ["Stopped","TimeOut"]:
                                execResult = TaskCenterService.__execTaskCaseJob(caseId)
                                if not execResult.getSuccess():
                                    #set instance db
                                    taskGlobalStatus = execResult.getMessage()
                                    return result
                            else:
                                logger.error("Task instance [{0}] is stopped".format(args.get("instanceId")))
                                taskGlobalStatus = dataResult.getMessage()[0].get("status")
                                return result
                        taskGlobalStatus = "Success"
                        result.setSuccess(True)
                        return result
        except Exception,err:
            logger.error("Exception:{0}".format(traceback.format_exc()))
            return result
        finally:
            args.setdefault("build_end", datetime.datetime.now())
            args.setdefault("status",taskGlobalStatus)
            return TestCaseInstanceDaoInterface().updateTestInstance(args)

    @staticmehtod
    @AdminDecoratorServer.execImplDecorator()
    def __execTaskCaseJob(caseId):
        return DataResult()

    @AdminDecoratorServer.execImplDecorator()
    def sendTask(self):
        args={}
        args.setdefault("limit",SystemConfig.maxThreadSize)
        dataResult = TaskMetaqInfoDaoInterface().getWaitingTaskInfos(args)
        if dataResult.getSuccess():
            logger.info("send Task start:{0}".format(dataResult.getMessage()))
            #目前支持local执行,后期可支持远程consumer或者jenkins
            requests = threadpool.makeRequests(self.__sendTaskJob,dataResult.getMessage())
            for req in requests:
                time.sleep(0.1)
                pool.putRequest(req)
            pool.wait()
            return dataResult
        else:
            logger.error("get waiting task failure:{0}".format(dataResult.getMessage()))
            return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def stopTask(self,args):
        return self.taskMetaqInfoDaoInterface.addTaskInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def startTask(self,args):
        return self.taskMetaqInfoDaoInterface.addTaskInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def execTask(self,args):
        return self.taskMetaqInfoDaoInterface.addTaskInfo(args)
