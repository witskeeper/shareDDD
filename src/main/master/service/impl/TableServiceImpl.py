# -*- coding: utf-8 -*-

import json, itertools
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
        result = self.TableDaoInterface.getColumnListByTableId(args)
        message = []
        for row in result.getMessage():
            links = row["links"]
            if links is None:
                row["links"] = []
            else:
                link_str = links.split('|')
                link_json = [json.loads(l) for l in link_str]
                row["links"] =link_json
            message.append(row)
        result.setMessage(message)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByTableName(self, args):
        return self.TableDaoInterface.getColumnListByTableName(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumn(self, args):
        return self.TableDaoInterface.editColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnRemarkById(self, args, is_execute_many=False):
        return self.TableDaoInterface.editColumnRemarkById(args, is_execute_many)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnTypeById(self, args, is_execute_many=False):
        return self.TableDaoInterface.editColumnTypeById(args, is_execute_many)

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
                tableDict["cName"] = i["TABLE_COMMENT"]
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
                        remark = j["COLUMN_COMMENT"]
                        columnDict["remark"] = remark
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
        tables_diff_list = list(tables_diff)
        tables_diff_dict = [i for i in tables_src if tables_diff_list.count(i["TABLE_NAME"]) > 0 ]
        # 获取需要比较表字段的数据表，排除上面差集的数据表
        tables_compare = set(tables_src_list) -  tables_diff
        # 增加表
        logTableList = []
        for i in tables_diff_dict:
            db_table = i["TABLE_NAME"]
            tableDict = {}
            tableDict["DBId"] = DBId
            tableDict["cName"] = i["TABLE_COMMENT"]
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
                columnDict = {}
                columnDict["tableId"] = tableId
                columnDict["cName"] = ""
                columnDict["eName"] = column_info[0]["COLUMN_NAME"]
                columnDict["type"] = column_info[0]["COLUMN_TYPE"]
                remark = column_info[0]["COLUMN_COMMENT"]
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
    def getSearchByColumnRemark(self, args):
        logger.info(args)
        content = args
        args = {}
        args.setdefault("DBId", content["DBId"])
        args.setdefault("remark", '%{}%'.format((content["content"].encode('utf-8'))[1:]))
        logger.info(args)
        return self.TableDaoInterface.getSearchByColumnRemark(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDBLog(self, DBId, content, userId=0, type=0):
        # todo 默认无用户
        args = {}
        args.setdefault("userId", userId)
        args.setdefault("DBId", DBId)
        if type == 0:
            content = [c.encode('utf8') for c in content]
            concat_content = "添加了{}".format("、".join(content))
        elif type == 1:
            # content = [c.encode('utf8') for c in content]
            concat_content = "更新了{}".format("、".join(content))

        args.setdefault("content", concat_content)
        logger.info(args)
        return self.TableDaoInterface.addDBLog(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDBLogList(self, DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.TableDaoInterface.getDBLogList(args)

    @AdminDecoratorServer.execImplDecorator()
    def addColumnLink(self, args):
        return self.TableDaoInterface.addColumnLink(args)

    @AdminDecoratorServer.execImplDecorator()
    def getLinkTableList(self, DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.TableDaoInterface.getLinkTableList(args)

    @AdminDecoratorServer.execImplDecorator()
    def getLinkColumnList(self, tableId):
        args = {}
        args.setdefault("tableId", tableId)
        return self.TableDaoInterface.getLinkColumnList(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableListByTableName(self, content):
        args = {}
        args.setdefault("DBId", content["id"])
        args.setdefault("eName", '%{}%'.format(content["content"]))
        return self.TableDaoInterface.getTableListByTableName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByColName(self, content):
        args = {}
        args.setdefault("tableId", content["id"])
        args.setdefault("eName", '%{}%'.format(content["content"]))
        return self.TableDaoInterface.getColumnListByColName(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTableRoute(self, args):
        return self.TableDaoInterface.addTableRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDataNode(self, args):
        return self.TableDaoInterface.addDataNode(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDataRoute(self, args):
        return self.TableDaoInterface.addDataRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableRouteList(self, table_id):
        args = {}
        args.setdefault("table_id", table_id)
        result = self.TableDaoInterface.getTableRouteList(args)
        route = result.getMessage()
        message = []
        route_group = itertools.groupby(route, key=lambda x: x["route_id"])
        for key,value in route_group:
            s = {}
            s.setdefault("key", key)
            s.setdefault("route", list(value))
            logger.info(s)
            message.append(s)
        result.setMessage(message)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def updateComment(self, args):
        result = DataResult()
        result.setSuccess(True)
        user_id = 0
        table_id = args["id"]
        db_id = args["DBId"]
        # 获取表信息
        table_info = (self.getTableInfoById(table_id)).getMessage()
        table_e_name = table_info[0]["eName"]
        table_c_name = table_info[0]["cName"]
        # 获取原库的表信息
        table_info_src = (self.getTableComment(db_id, table_e_name)).getMessage()
        table_c_name_src = table_info_src[0]["TABLE_COMMENT"]
        flag_table = False
        table_content = []
        # 对比表信息
        if table_c_name != table_c_name_src:
            flag_table = True
            content = "表{}的【中文名】从 [{}] 变成 [{}]".format(table_e_name.encode("utf8"), table_c_name.encode("utf8"), table_c_name_src.encode("utf8"))
            table_content.append(content)
        if flag_table:
            self.editTableCommentById(table_id, table_c_name_src)
            self.addDBLog(db_id, table_content, user_id, 1)
        # 对比字段信息
        # getSynchronizeTable
        c_args = {}
        c_args.setdefault("eName", table_e_name)
        c_args.setdefault("DBId", db_id)
        # 获取表字段信息
        column_info = (self.getColumnListByTableName(c_args)).getMessage()
         # 获取原库的表字段信息
        db_src = self.getDBSrcInfo(db_id)
        interface_table = self.TableDaoInterface
        cs_args = {}
        cs_args.setdefault("schemaName", db_src["db"])
        cs_args.setdefault("tableName", table_e_name)
        column_info_src = interface_table.getSynchronizeTable(cs_args, **db_src).getMessage()
        column_info = [{"name":i["eName"],"type":i["type"],"remark":i["remark"],"id":i["id"]} for i in column_info]
        column_info_src = [{"name":i["COLUMN_NAME"],"type":i["COLUMN_TYPE"],"remark":i["COLUMN_COMMENT"]}
                           for i in column_info_src]
        column_info = sorted(column_info, key=lambda x:x["name"])
        column_info_src = sorted(column_info_src, key=lambda x:x["name"])
        flag_column = False
        column_content = []
        update_column_type = []
        update_column_remark = []
        if len(column_info) == len(column_info_src):
            flag_column = True
        else:
            result.setSuccess(False)
            result.setMessage("当前表的字段数和源库中不一致，请先同步表信息")
        if flag_column:
            for x,y in zip(column_info,column_info_src):
                one_flag = False
                if x["name"] == y["name"]:
                    one_flag = True
                if one_flag:
                    if x["type"] != y["type"]:
                        args_type = {}
                        args_type.setdefault("id", x["id"])
                        args_type.setdefault("val", y["type"])
                        update_column_type.append(args_type)
                        content = "字段{}.{}的【类型】从 [{}] 变成 [{}]".format(table_e_name.encode("utf8"), x["name"].encode("utf8"),
                                                               x["type"].encode("utf8"),y["type"].encode("utf8"))
                        column_content.append(content)
                    if x["remark"] != y["remark"]:
                        args_remark = {}
                        args_remark.setdefault("id", x["id"])
                        args_remark.setdefault("val", y["remark"])
                        update_column_remark.append(args_remark)
                        content = "字段{}.{}的【备注】从 [{}] 变成 [{}]".format(table_e_name.encode("utf8"), x["name"].encode("utf8"),
                                                               x["remark"].encode("utf8"), y["remark"].encode("utf8"))
                        column_content.append(content)
        if flag_column:
            self.editColumnTypeById(update_column_type, True)
            self.editColumnRemarkById(update_column_remark, True)
            if len(column_content) > 0:
                self.addDBLog(db_id, column_content, user_id, 1)

        return result

    @AdminDecoratorServer.execImplDecorator()
    def getTableComment(self, db_id, table_name):
        db_src = self.getDBSrcInfo(db_id)
        db_schema = db_src["db"]

        args = {}
        args.setdefault("schemaName", db_schema)
        args.setdefault("tableName", table_name)

        return self.TableDaoInterface.getTableComment(args, **db_src)

    @AdminDecoratorServer.execImplDecorator()
    def editTableCommentById(self, id, table_c_name):
        args = {}
        args.setdefault("id", id)
        args.setdefault("cName", table_c_name)
        return self.TableDaoInterface.editTableCommentById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDBSrcInfo(self, db_id):
        interface_db = self.DatabaseDaoInterface
        db_info = interface_db.getDatabaseInfoById({"id": db_id}).getMessage()
        db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                  'db': db_info[0]["schemaName"], 'port': db_info[0]["port"]}
        return db_src
