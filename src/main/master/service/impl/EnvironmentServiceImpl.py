# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.EnvironmentDao import EnvironmentDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('EnvironmentServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"EnvironmentServiceImpl.log")

class EnvironmentService(object):

    def __init__(self):
        self.EnvironmentDaoInterface = EnvironmentDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addEnvironmentItem(self,args):
        if "datatemplate" not in args:
            args.setdefault("template",None)
        else:
            if not isinstance(args.get("datatemplate"),dict):
                try:
                    #验证data模板是否为json
                    logger.info("datatemplate is not dict:{0}".format(args.get("datatemplate")))
                    json.loads(args.get("datatemplate"))
                    args.setdefault("template", args.get("datatemplate"))
                except Exception,err:
                    logger.error(traceback.format_exc())
                    dataResult = DataResult()
                    dataResult.setMessage("datatemplate param [{0}]is invalid, must be dict".format(args.get("datatemplate")))
                    dataResult.setSuccess(False)
                    return dataResult
            else:
                logger.info("datatemplate is dict:{0}".format(args.get("datatemplate")))
                datatemplateJSONString = json.dumps(args.get("datatemplate"))
                args.setdefault("template",datatemplateJSONString)
        if "dbname" not in args:
            args.setdefault("dbname",None)
        if "dbhostname" not in args:
            args.setdefault("dbhostname",None)
        if "dbport" not in args:
            args.setdefault("dbport",None)
        if "dbusername" not in args:
            args.setdefault("dbusername",None)
        if "dbpasswd" not in args:
            args.setdefault("dbpasswd",None)
        return self.EnvironmentDaoInterface.addEnvironmentItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def getEnvironmentInfoById(self,envId):
        args={}
        args.setdefault("envId",envId)
        return self.EnvironmentDaoInterface.getEnvironmentInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteEnvironmentItem(self,args):
        return self.EnvironmentDaoInterface.deleteEnvironmentItem(args)

