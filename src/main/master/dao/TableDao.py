# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TableMapper import TableSQLMapper

#set log
logger = Log('TableDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TableDao.log")

class TableDaoInterface:

    def addTable(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def discardTableByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addColumn(self,args,is_execute_many=False):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getColumnInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnRemarkById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnDiscardById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def isInitSynchronize(self, args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSynchronizeDatabase(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeTable(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeColumn(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def initSynchronizeDatabase(self, args):
        #  todo 没有sql
        logger.info(inspect.stack()[0][3])
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def SynchronizeDatabase(self, args):
        #  todo 没有sql
        logger.info(inspect.stack()[0][3])
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def addDataRoute(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def deleteDataRoute(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDataRouteInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDataRouteList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editDataRoute(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getSearchByTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByTableColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addDBLog(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDBLogList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TableSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()
