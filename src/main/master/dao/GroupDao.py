# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.GroupMapper import GroupSQLMapper

#set log
logger = Log('GroupDao')
logger.write_to_file(SystemConfig.logPathPrefix+"GroupDao.log")

class GroupDaoInterface:

    def addGroup(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = GroupSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getGroupInfoByProjectId(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = GroupSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = GroupSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getGroupInfoByName(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = GroupSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()


