# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.LoginDao import LoginDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('LoginServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"LoginServiceImpl.log")

class LoginService(object):

    def __init__(self):
        self.LoginDaoInterface = LoginDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addUser(self,args):
        logger.error(args)
        logger.error(type(args))
        return self.LoginDaoInterface.addUser(args)
