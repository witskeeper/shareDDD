# -*- coding: utf-8 -*-

# todo 注意关键字重名，如database,schema
# CREATE TABLE `databaseManage` (
# `id` int(11) NOT NULL auto_increment,
# `name` varchar(255) NOT NULL,
# `host` varchar(255) NOT NULL,
# `port` int(4) default 0 NOT NULL,
# `username` varchar(32) NOT NULL,
# `password` varchar(128) NOT NULL,
# `schemaName` varchar(32) NOT NULL,
# `businessUnit` TINYINT(4) default 0 NOT NULL,
# `productUnit` TINYINT(4) default 0 NOT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `tableGroup` (
# `id` int(11) NOT NULL auto_increment,
# `DBId` int(11) default 0 NOT NULL,
# `name` varchar(64) NOT NULL,
# `isDefault` TINYINT(4) default 0 NOT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `tableGroupRelation` (
# `id` int(11) NOT NULL auto_increment,
# `tableId` int(11) default 0 NOT NULL,
# `groupId` int(11) default 0 NOT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class DatabaseSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addDatabaseSQL="""
        insert into databasemanage (name,host,port,username,password,schemaName,businessUnit,productUnit) 
        values (%(name)s,%(host)s,%(port)s,%(username)s,%(password)s,%(schemaName)s,%(businessUnit)s,%(productUnit)s)
        """

        deleteDatabaseSQL="""
        delete from databasemanage where id = %(id)s
        """
        getDatabaseInfoByIdSQL="""
        select * from databasemanage where id = %(id)s
        """
        getDatabaseListSQL="""
        select * from databasemanage where businessUnit = %(businessUnit)s 
        """

        editDatabaseSQL="""
        update databasemanage set name=%(name)s,host=%(host)s,port=%(port)s,username=%(username)s,password=%(password)s,
        schemaName=%(schemaName)s,businessUnit=%(businessUnit)s,productUnit=%(productUnit)s where id=%(id)s
        """

        addTableGroupSQL = """
        insert into tablegroup (DBId,name,isDefault) 
        values (%(DBId)s,%(name)s,%(isDefault)s)
        """

        deleteTableGroupSQL = """
        delete from tablegroup where id = %(id)s
        """

        getTableGroupInfoByIdSQL = """
        select * from tablegroup where id = %(id)s
        """

        getTableGroupInfoByNameSQL = """
        select * from tablegroup where DBId = %(DBId)s and name = %(name)s
        """

        getTableGroupListSQL = """
        select * from tablegroup where DBId = %(DBId)s 
        """

        editTableGroupSQL = """
        update tablegroup set DBId=%(DBId)s,name=%(name)s where id=%(id)s
        """

        addTableGroupRelationSQL = """
        insert into tablegrouprelation (tableId,groupId) 
        values (%(tableId)s,%(groupId)s)
        """

        deleteTableGroupRelationSQL = """
        delete from tablegrouprelation where id = %(id)s
        """

        getTableGroupRelationListSQL = """
        select tgr.*,tg.*,t.eName,t.cName from tablegrouprelation tgr join tablegroup tg 
         on tgr.groupId = tg.id join dbtable t on t.id = tgr.tableId
         where tg.DBId = %(DBId)s 
        """

        updateTableGroupRelationSQL = """
        update tablegrouprelation set groupId=%(groupId)s where find_in_set(id,%(ids)s) 
        """

        updateTableGroupRelationByGroupIdSQL = """
        update tablegrouprelation set groupId=%(defaultId)s where groupId=%(groupId)s 
        """

        deleteTableGroupByDBSQL = """
        DELETE FROM tableGroup where DBId = %(id)s; 
        """

        deleteTableGroupRelationByDBSQL = """
        DELETE FROM tableGroupRelation where tableId in (SELECT id from dbtable where DBId = %(id)s); 
        """

        #SET SQL FOR DAO
        self.data.setdefault("addDatabase",addDatabaseSQL)
        self.data.setdefault("deleteDatabase",deleteDatabaseSQL)
        self.data.setdefault("getDatabaseInfoById",getDatabaseInfoByIdSQL)
        self.data.setdefault("getDatabaseList", getDatabaseListSQL)
        self.data.setdefault("editDatabase", editDatabaseSQL)

        self.data.setdefault("addTableGroup", addTableGroupSQL)
        self.data.setdefault("deleteTableGroup", deleteTableGroupSQL)
        self.data.setdefault("getTableGroupInfoById", getTableGroupInfoByIdSQL)
        self.data.setdefault("getTableGroupInfoByName", getTableGroupInfoByNameSQL)
        self.data.setdefault("getTableGroupList", getTableGroupListSQL)
        self.data.setdefault("editTableGroup", editTableGroupSQL)

        self.data.setdefault("addTableGroupRelation", addTableGroupRelationSQL)
        self.data.setdefault("deleteTableGroupRelation", deleteTableGroupRelationSQL)
        self.data.setdefault("getTableGroupRelationList", getTableGroupRelationListSQL)
        self.data.setdefault("updateTableGroupRelation", updateTableGroupRelationSQL)
        self.data.setdefault("updateTableGroupRelationByGroupId", updateTableGroupRelationByGroupIdSQL)

        self.data.setdefault("deleteTableGroupByDB", deleteTableGroupByDBSQL)
        self.data.setdefault("deleteTableGroupRelationByDB", deleteTableGroupRelationByDBSQL)


