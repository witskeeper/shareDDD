# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.UserDao import UserDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('UserServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"UserServiceImpl.log")

class UserService(object):

    def __init__(self):
        self.userDaoInterface = UserDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addUser(self,args):
        return self.userDaoInterface.addUser(args)

    @AdminDecoratorServer.execImplDecorator()
    def getUserInfo(self,userName):
        args={}
        #此处的user_name必须与sql定义中参数一致，即 %(user_name)s
        args.setdefault("userName",userName)
        return self.userDaoInterface.getUserInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteUser(self,args):
        return self.userDaoInterface.deleteUser(args)

    @AdminDecoratorServer.execImplDecorator()
    def getUserInfoById(self,id):
        args={}
        #此处的user_name必须与sql定义中参数一致，即 %(user_name)s
        args.setdefault("userId",id)
        return self.userDaoInterface.getUserInfo(args)

