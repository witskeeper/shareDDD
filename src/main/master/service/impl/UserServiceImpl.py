# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.UserDao import UserDaoInterface

#set log
logger = Log('UserServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"UserServiceImpl.log")

class UserService(object):

    def __init__(self):
        self.userDaoInterface = UserDaoInterface()

    def addUser(self,args):
        try:
            return self.userDaoInterface.addUser(args)
        except Exception,e:
            dataResult = DataResult()
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult

    def getUserInfo(self,userName):
        try:
            args={}
            #此处的user_name必须与sql定义中参数一致，即 %(user_name)s
            args.setdefault("user_name",userName)
            return self.userDaoInterface.getUserInfo(args)
        except Exception,e:
            dataResult = DataResult()
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult

    def deleteUser(self,userName):
        try:
            args={}
            args.setdefault("user_name", userName)
            return self.userDaoInterface.deleteUser(args)
        except Exception, e:
            dataResult = DataResult()
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            return dataResult
