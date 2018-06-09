# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.DatabaseMapper import DatabaseSQLMapper

#set log
logger = Log('DatabaseDao')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseDao.log")

class DatabaseDaoInterface:

    def addDatabase(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def deleteDatabase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDatabaseInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabaseList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editDatabase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()
    
    def addTableGroup(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTableGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addTableGroupRelation(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroupRelation(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupRelationList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def updateTableGroupRelation(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTableGroupRelationByGroupId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTableGroupByDB(self, args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTableGroupRelationByDB(self, args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()


