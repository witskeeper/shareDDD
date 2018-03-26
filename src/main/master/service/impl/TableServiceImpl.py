# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TableDao import TableDaoInterface
from src.main.master.dao.DatabaseDao import DatabaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TableServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TableServiceImpl.log")

class TableService(object):

    def __init__(self):
        self.TableDaoInterface = TableDaoInterface()
        self.DatabaseDaoInterface = DatabaseDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTable(self,args):
        return self.TableDaoInterface.addTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTable(self,args):
        return self.TableDaoInterface.deleteTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableInfoById(self,id):
        args={}
        args.setdefault("id",id)
        return self.TableDaoInterface.getTableInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableInfoByName(self, args):
        return self.TableDaoInterface.getTableInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableList(self,DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.TableDaoInterface.getTableList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTable(self, args):
        return self.TableDaoInterface.editTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTableByName(self, args):
        return self.TableDaoInterface.editTableByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def discardTableByName(self, args):
        return self.TableDaoInterface.discardTableByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def addColumn(self, args):
        return self.TableDaoInterface.addColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteColumn(self, args):
        return self.TableDaoInterface.deleteColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnInfoById(self, productId):
        args = {}
        args.setdefault("id", productId)
        return self.TableDaoInterface.getColumnInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByTableId(self, TableId):
        args = {}
        args.setdefault("tableId", TableId)
        return self.TableDaoInterface.getColumnListByTableId(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByTableName(self, args):
        return self.TableDaoInterface.getColumnListByTableName(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumn(self, args):
        return self.TableDaoInterface.editColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnRemarkById(self, args):
        return self.TableDaoInterface.editColumnRemarkById(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnDiscardById(self, args):
        return self.TableDaoInterface.editColumnDiscardById(args)

    @AdminDecoratorServer.execImplDecorator()
    def isInitSynchronize(self, DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.TableDaoInterface.isInitSynchronize(args)

    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeDatabase(self, args):
        # 初始化同步，先同步所有表，再同步表里的所有字段
        interface_table = self.TableDaoInterface
        interface_db = self.DatabaseDaoInterface
        DBId = args["id"]
        count_info = self.isInitSynchronize(DBId)
        count = (count_info.getMessage())[0]["tableCount"]
        if count == 0:
            db_info = interface_db.getDatabaseInfoById({"id":DBId}).getMessage()
            db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                      'db': db_info[0]["schemaName"], 'port': db_info[0]["port"]}
            db_schema = db_info[0]["schemaName"]
            args = {}
            args.setdefault("schemaName", db_schema)
            tables = interface_table.getSynchronizeDatabase(args,**db_src).getMessage()
            insertTableList = []
            insertColumnList = []
            insertGroupList = []
            logTableList = []
            for i in tables:
                db_table = i["TABLE_NAME"]
                tableDict = {}
                tableDict["DBId"] = DBId
                tableDict["cName"] = ""
                tableDict["eName"] = db_table
                tableDict["remark"] = ""
                tableDict["is_discarded"] = 0
                insertTableList.append(tableDict)
                logTableList.append(db_table)
            result_table = interface_table.addTable(insertTableList, True).getSuccess()

            args = {}
            args["DBId"] = DBId
            args["name"] = "未分组"
            logger.info(interface_db.getTableGroupInfoByName(args).getMessage())
            groupId = (interface_db.getTableGroupInfoByName(args).getMessage())[0]["id"]
            if result_table:
                args = {}
                args.setdefault("DBId", DBId)
                tables = interface_table.getTableList(args).getMessage()
                for i in tables:
                    tableId = i["id"]
                    db_table = i["eName"]
                    args = {}
                    args.setdefault("schemaName", db_schema)
                    args.setdefault("tableName", db_table)
                    columns = interface_table.getSynchronizeTable(args,**db_src).getMessage()
                    relationDict = {}
                    relationDict["tableId"] = tableId
                    relationDict["groupId"] = groupId
                    interface_db.addTableGroupRelation(relationDict)
                    for j in columns:
                        columnDict = {}
                        columnDict["tableId"] = tableId
                        columnDict["cName"] = ""
                        columnDict["eName"] = j["COLUMN_NAME"]
                        columnDict["type"] = j["COLUMN_TYPE"]
                        columnDict["remark"] = j["COLUMN_COMMENT"]
                        columnDict["is_discarded"] = 0
                        insertColumnList.append(columnDict)

                interface_table.addColumn(insertColumnList, True)

                # 输出log记录信息都是表
                return self.addDBLog(DBId, logTableList)

            else:
                return result_table
        else:
            return count_info

    @AdminDecoratorServer.execImplDecorator()
    def synchronizeDatabase(self, args):
        # 后续同步，比较表差和字段差
        interface_table = self.TableDaoInterface
        interface_db = self.DatabaseDaoInterface
        DBId = args["id"]
        db_info = interface_db.getDatabaseInfoById({"id": DBId}).getMessage()
        db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                  'db': db_info[0]["schemaName"], 'port': db_info[0]["port"]}
        db_schema = db_info[0]["schemaName"]
        args = {}
        args.setdefault("schemaName", db_schema)
        tables_src = interface_table.getSynchronizeDatabase(args, **db_src).getMessage()
        tables_src_list = [i["TABLE_NAME"] for i in tables_src]
        tables_dest = self.getTableList(DBId).getMessage()
        tables_dest_list = [i["eName"] for i in tables_dest]
        # 获取源数据库和目标数据库的差集，用于增加整表
        tables_diff = set(tables_src_list) - set(tables_dest_list)
        # 获取需要比较表字段的数据表，排除上面差集的数据表
        tables_compare = set(tables_src_list) -  tables_diff
        # 增加表
        logTableList = []
        for i in tables_diff:
            db_table = i
            tableDict = {}
            tableDict["DBId"] = DBId
            tableDict["cName"] = ""
            tableDict["eName"] = db_table
            tableDict["remark"] = ""
            tableDict["is_discarded"] = 0
            logTableList.append(db_table.encode('utf-8'))
            result_table = interface_table.addTable(tableDict).getSuccess()
            insertColumnList = []
            args = {}
            args["DBId"] = DBId
            args["name"] = "未分组"
            groupinfo = interface_db.getTableGroupInfoByName(args)
            groupId = (interface_db.getTableGroupInfoByName(args).getMessage())[0]["id"]
            args = {}
            args.setdefault("DBId", DBId)
            args.setdefault("eName", db_table)
            tables = interface_table.getTableInfoByName(args).getMessage()
            tableId = tables[0]["id"]
            # 添加默认表关系
            relationDict = {}
            relationDict["tableId"] = tableId
            relationDict["groupId"] = groupId
            logger.info(relationDict)
            # 调用和报错
            interface_db.addTableGroupRelation(relationDict)

            if result_table:
                args = {}
                args.setdefault("DBId", DBId)
                args.setdefault("eName", db_table)
                tables = interface_table.getTableInfoByName(args).getMessage()
                tableId = tables[0]["id"]
                db_table = tables[0]["eName"]

                # 获取源数据库表字段
                args = {}
                args.setdefault("schemaName", db_schema)
                args.setdefault("tableName", db_table)
                columns = interface_table.getSynchronizeTable(args, **db_src).getMessage()
                for j in columns:
                    columnDict = {}
                    columnDict["tableId"] = tableId
                    columnDict["cName"] = ""
                    columnDict["eName"] = j["COLUMN_NAME"]
                    columnDict["type"] = j["COLUMN_TYPE"]
                    remark = j["COLUMN_COMMENT"]
                    if remark == "":
                        columnDict["remark"] = "-"
                    else:
                        columnDict["remark"] = remark
                    columnDict["is_discarded"] = 0
                    insertColumnList.append(columnDict)
                interface_table.addColumn(insertColumnList, True)

        # 比较表，根据缺少的字段，增加字段
        logColumnList = []
        for i in tables_compare:
            args = {}
            args.setdefault("DBId", DBId)
            args.setdefault("eName", i)
            table_info = interface_table.getTableInfoByName(args).getMessage()
            tableId = table_info[0]["id"]
            db_table = table_info[0]["eName"]
            args = {}
            args.setdefault("schemaName", db_schema)
            args.setdefault("tableName", db_table)
            columns_src = interface_table.getSynchronizeTable(args, **db_src).getMessage()
            columns_src_list = [i["COLUMN_NAME"] for i in columns_src]
            columns_dest = self.getColumnListByTableId(tableId).getMessage()
            columns_dest_list = [i["eName"] for i in columns_dest]
            columns_diff = set(columns_src_list) - set(columns_dest_list)

            for j in columns_diff:
                args = {}
                args.setdefault("schemaName", db_schema)
                args.setdefault("tableName", db_table)
                args.setdefault("columnName", j)
                column_info = interface_table.getSynchronizeColumn(args, **db_src).getMessage()
                print(column_info)
                columnDict = {}
                columnDict["tableId"] = tableId
                columnDict["cName"] = ""
                columnDict["eName"] = column_info[0]["COLUMN_NAME"]
                columnDict["type"] = column_info[0]["COLUMN_TYPE"]
                remark = column_info[0]["COLUMN_COMMENT"]
                if remark == "":
                    columnDict["remark"] = "-"
                else:
                    columnDict["remark"] = remark
                columnDict["is_discarded"] = 0
                logColumnName = "{}.{}".format(db_table, columnDict["eName"])
                logColumnList.append(logColumnName)
                interface_table.addColumn(columnDict)

        interface_db.getDatabaseInfoById({"id": DBId})

        # 增加log信息
        return self.addDBLog(DBId, logTableList+logColumnList)


    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeTable(self, schemaName, tableName):
        # 多个表？不同数据库的表
        args = {}
        args.setdefault("schemaName", schemaName)
        args.setdefault("tableName", tableName)
        return self.TableDaoInterface.initSynchronizeTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeColumn(self, schemaName, tableName, columnName):
        args = {}
        args.setdefault("schemaName", schemaName)
        args.setdefault("tableName", tableName)
        args.setdefault("columnName", columnName)
        return self.TableDaoInterface.initSynchronizeColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeDatabase(self, args, **kwargs):
        print(kwargs)
        # args = {}
        # args.setdefault("schemaName", db_schema)
        return self.TableDaoInterface.getSynchronizeDatabase(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeTable(self, args, **kwargs):
        return self.TableDaoInterface.getSynchronizeTable(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeColumn(self, args, **kwargs):
        return self.TableDaoInterface.getSynchronizeColumn(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def addDataRoute(self, args):
        return self.TableDaoInterface.addDataRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteDataRoute(self, args):
        return self.TableDaoInterface.deleteDataRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDataRouteInfoById(self, dataRouteId):
        args = {}
        args.setdefault("id", dataRouteId)
        return self.TableDaoInterface.getDataRouteInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDataRouteList(self, tableId):
        # todo businessUnit=2
        args = {}
        args.setdefault("tableId", tableId)
        return self.TableDaoInterface.getDataRouteList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editDataRoute(self, args):
        return self.TableDaoInterface.editDataRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByTable(self, args):
        content = args
        args = {}
        args.setdefault("DBId", content["DBId"])
        args.setdefault("tname", '%{}%'.format(content["content"]))
        logger.info(args)
        return self.TableDaoInterface.getSearchByTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByTableColumn(self, args):
        content = args
        search = content["content"].split('.')
        args = {}
        args.setdefault("DBId", content["DBId"])
        args.setdefault("tname", search[0])
        args.setdefault("cname", '%{}%'.format(search[1]))
        logger.info(args)
        return self.TableDaoInterface.getSearchByTableColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByColumn(self, args):
        content = args
        args = {}
        args.setdefault("DBId", content["DBId"])
        args.setdefault("cname", '%{}%'.format(content["content"][1:]))
        logger.info(args)
        return self.TableDaoInterface.getSearchByColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDBLog(self, DBId, content, userId=0):
        # todo 默认无用户
        args = {}
        args.setdefault("userId", userId)
        args.setdefault("DBId", DBId)
        concat_content = "添加了{}".format("、".join(content))
        args.setdefault("content", concat_content)
        logger.info(args)
        return self.TableDaoInterface.addDBLog(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDBLogList(self, DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.TableDaoInterface.getDBLogList(args)