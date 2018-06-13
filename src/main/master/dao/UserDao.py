# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.UserMapper import UserSQLMapper

#set log
logger = Log('UserDao')
logger.write_to_file(SystemConfig.logPathPrefix+"UserDao.log")

class UserDaoInterface:

    def addUser(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getUserInfo(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteUser(self,args):
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getUserInfoById(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteUserInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addSysUser(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getSysUserList(self):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql)
        return daoOperate.read()

    def getSysUserInfoByName(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteSysUserInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = UserSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()