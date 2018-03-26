# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.DatabaseDao import DatabaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.service.impl.TableServiceImpl import TableService

#set log
logger = Log('DatabaseServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseServiceImpl.log")

class DatabaseService(object):

    def __init__(self):
        self.DatabaseDaoInterface = DatabaseDaoInterface()
        self.result = DataResult()
        self.TableService = TableService()

    @AdminDecoratorServer.execImplDecorator()
    def addDatabase(self,args):
        result = self.DatabaseDaoInterface.addDatabase(args)
        # 添加默认表分组
        DBId = result.getMessage()
        groupDict = {}
        groupDict["DBId"] = DBId
        groupDict["name"] = "未分组"
        groupDict["isDefault"] = 1
        self.addTableGroup(groupDict)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def deleteDatabase(self,args):
        # todo 删除关联关系
        # self.deleteTableGroup()
        # self.deleteTableGroupRelation()
        # self.TableService.deleteTable()
        # self.TableService.deleteColumn()
        return self.DatabaseDaoInterface.deleteDatabase(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabaseInfoById(self,databaseId):
        args={}
        args.setdefault("id",databaseId)
        return self.DatabaseDaoInterface.getDatabaseInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabaseList(self):
        # todo businessUnit=2
        args = {}
        args.setdefault("businessUnit", 2)
        return self.DatabaseDaoInterface.getDatabaseList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editDatabase(self, args):
        return self.DatabaseDaoInterface.editDatabase(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTableGroup(self, args):
        return self.DatabaseDaoInterface.addTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroup(self, args):
        if args["isDefault"] == 1:
            self.result.setMessage("默认分组不能删除")
            return self.result
        else:
            #todo 创建事务
            groupId = args["id"]
            DBId = args["DBId"]
            name = "未分组"
            defaultId = (self.getTableGroupInfoByName(DBId, name).getMessage())[0]["id"]
            self.updateTableGroupRelationByGroupId(groupId, defaultId)
            return self.DatabaseDaoInterface.deleteTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupInfoById(self, groupId):
        args = {}
        args.setdefault("id", groupId)
        return self.DatabaseDaoInterface.getTableGroupInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupInfoByName(self, DBId, name):
        args = {}
        args.setdefault("DBId", DBId)
        args.setdefault("name", name)
        return self.DatabaseDaoInterface.getTableGroupInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupList(self, DBId):
        args = {}
        args.setdefault("DBId", DBId)
        return self.DatabaseDaoInterface.getTableGroupList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTableGroup(self, args):
        return self.DatabaseDaoInterface.editTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTableGroupRelation(self, args):
        return self.DatabaseDaoInterface.addTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroupRelation(self, relationId):
        args = {}
        args.setdefault("id", relationId)
        return self.DatabaseDaoInterface.deleteTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupRelationList(self, DBId):
        from itertools import groupby
        args = {}
        args.setdefault("DBId", DBId)
        self.result = self.DatabaseDaoInterface.getTableGroupRelationList(args)
        dbName = (self.getDatabaseInfoById(DBId).getMessage())[0]["name"]
        # 先排序再分组，不然会被隔开
        handleRet = sorted(self.result.getMessage(), key= lambda x: x["groupId"])
        handleRet = groupby(handleRet, key= lambda x: x["groupId"])
        endRet = []
        index = 0
        for key, group in handleRet:
            groupDict = {}
            #  先转为list
            group=list(group)
            groupDict.setdefault("title", group[0]["name"])
            logger.info(group)
            groupDict.setdefault("children", [{"title":l["eName"],"id":l["id"],"tableId":l["tableId"]} for l in group])
            # 用于设置默认展开
            if index == 0:
                groupDict.setdefault("expand", True)
                itmeDict = groupDict["children"][0]
                itmeDict.setdefault("selected", True)
                logger.info(itmeDict)
            index += 1
            endRet.append(groupDict)
        message = {}
        message.setdefault("dbName", dbName)
        message.setdefault("groupInfo", endRet)
        self.result.setMessage(message)
        return self.result

    @AdminDecoratorServer.execImplDecorator()
    def updateTableGroupRelation(self, infos):
        args = {}
        ids = ",".join(infos["tables"])
        args.setdefault("DBId", int(infos["DBId"]))
        args.setdefault("groupId", infos["groupId"])
        args.setdefault("ids", ids)
        logger.info(args)
        return self.DatabaseDaoInterface.updateTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTableGroupRelationByGroupId(self, groupId, defaultId):
        args = {}
        args.setdefault("groupId", groupId)
        args.setdefault("defaultId", defaultId)
        logger.info(args)
        return self.DatabaseDaoInterface.updateTableGroupRelationByGroupId(args)
