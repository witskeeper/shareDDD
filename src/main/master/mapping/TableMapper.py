# -*- coding: utf-8 -*-

# CREATE TABLE `DBTable` (
# `id` int(11) NOT NULL auto_increment,
# `DBId` int(11) default 0 NOT NULL,
# `cName` varchar(255) NOT NULL,
# `eName` varchar(255) NOT NULL,
# `remark` varchar(1024) NOT NULL,
# `is_discarded` TINYINT(4)  NOT NULL,
# `gmt_create` datetime DEFAULT NULL,
# `gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `DBColumn` (
# `id` int(11) NOT NULL auto_increment,
# `tableId` int(11) default 0 NOT NULL,
# `cName` varchar(255) NOT NULL,
# `eName` varchar(255) NOT NULL,
# `type` varchar(32) NOT NULL,
# `remark` varchar(1024)  NOT NULL,
# `is_discarded` TINYINT(4)  NOT NULL,
# `gmt_create` datetime DEFAULT NULL,
# `gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `dataRoute` (
# `id` int(11) NOT NULL auto_increment,
# `tableId` int(11) default 0 NOT NULL,
# `route` varchar(512) NOT NULL,
# `type` TINYINT(4) NOT NULL COMMENT '0 input, 1 output',
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class TableSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性,设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTableSQL="""
        insert into dbtable (DBId,cName,eName,remark,is_discarded,gmt_create,gmt_modify) 
        values (%(DBId)s,%(cName)s,%(eName)s,%(remark)s,%(is_discarded)s,now(),now())
        """

        deleteTableSQL="""
        delete from dbtable where id = %(id)s
        """

        getTableInfoByIdSQL="""
        select * from dbtable where id = %(id)s
        """

        getTableInfoByNameSQL = """
        select * from dbtable where DBId = %(DBId)s and eName = %(eName)s 
        """

        getTableListSQL="""
        select * from dbtable where DBId = %(DBId)s 
        """

        editTableSQL="""
        update dbtable set DBId=%(DBId)s,cName=%(cName)s,eName=%(eName)s,remark=%(remark)s,
        is_discarded=%(is_discarded)s,gmt_modify=%(gmt_modify)s where id=%(id)s
        """

        editTableByNameSQL = """
        update dbtable set cName=%(cName)s,remark=%(remark)s,
        gmt_modify=now() where DBId=%(DBId)s and eName=%(eName)s
        """

        discardTableByNameSQL = """
        update dbtable set is_discarded=1,
        gmt_modify=now() where DBId=%(DBId)s and eName=%(eName)s
        """

        addColumnSQL = """
        insert into dbcolumn (tableId,cName,eName,type,remark,is_discarded,gmt_create,gmt_modify) 
        values (%(tableId)s,%(cName)s,%(eName)s,%(type)s,%(remark)s,%(is_discarded)s,now(),now())
        """

        deleteColumnSQL = """
        delete from dbcolumn where id = %(id)s
        """
        getColumnInfoByIdSQL = """
        select * from dbcolumn where id = %(id)s
        """

        getColumnListByTableIdSQL = """
        select * from dbcolumn where tableId = %(tableId)s 
        """

        getColumnListByTableNameSQL = """
        select dc.* from dbcolumn dc join dbtable dt on dc.tableId = dt.id 
        where dt.eName=%(eName)s and dt.DBId=%(DBId)s
        """

        editColumnSQL = """
        update dbcolumn set tableId=%(tableId)s,cName=%(cName)s,eName=%(eName)s,type=%(type)s, 
        remark=%(remark)s,is_discarded=%(is_discarded)s,gmt_modify=now() where id=%(id)s
        """

        editColumnRemarkByIdSQL = """
        update dbcolumn set remark=%(val)s, gmt_modify=now() where id=%(id)s
        """

        editColumnDiscardByIdSQL = """
        update dbcolumn set is_discarded=%(val)s, gmt_modify=now() where id=%(id)s
        """

        isInitSynchronizeSQL = """
        SELECT count(*) as tableCount from dbtable WHERE DBId = %(DBId)s
        """

        getSynchronizeDatabaseSQL = """
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(schemaName)s;
        """

        getSynchronizeTableSQL = """
        SELECT COLUMN_NAME,COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schemaName)s and TABLE_NAME= %(tableName)s
        """

        getSynchronizeColumnSQL = """
        SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schemaName)s and TABLE_NAME = %(tableName)s and COLUMN_NAME = %(columnName)s
        """

        addDataRouteSQL="""
        insert into dataroute (tableId,route,type) 
        values (%(tableId)s,%(route)s,%(type)s)
        """

        deleteDataRouteSQL="""
        delete from dataroute where id = %(id)s
        """
        getDataRouteInfoByIdSQL="""
        select * from dataroute where id = %(id)s
        """
        getDataRouteListSQL="""
        select * from dataroute where tableId = %(tableId)s 
        """

        editDataRouteSQL="""
        update dataroute set tableId=%(tableId)s,route=%(route)s,type=%(type)s where id=%(id)s
        """

        getSearchByTableSQL="""
        SELECT t.id as uid, t.id,t.eName from dbtable t join dbcolumn c on t.id = c.tableId where DBId=%(DBId)s 
         and t.ename like %(tname)s GROUP BY t.id;
        """
        getSearchByTableColumnSQL = """
        SELECT c.id as uid, t.id,concat(t.eName,'.',c.eName) as eName from dbtable t join dbcolumn c on t.id = c.tableId 
         where DBId=%(DBId)s and t.ename = %(tname)s and c.eName like %(cname)s;
        """
        getSearchByColumnSQL = """
        SELECT c.id as uid, t.id,concat(t.eName,'.',c.eName) as eName from dbtable t join dbcolumn c on t.id = c.tableId 
         where DBId=%(DBId)s and c.ename like %(cname)s;
        """


        #SET SQL FOR DAO
        self.data.setdefault("addTable",addTableSQL)
        self.data.setdefault("deleteTable",deleteTableSQL)
        self.data.setdefault("getTableInfoById",getTableInfoByIdSQL)
        self.data.setdefault("getTableInfoByName",getTableInfoByNameSQL)
        self.data.setdefault("getTableList", getTableListSQL)
        self.data.setdefault("editTable", editTableSQL)
        self.data.setdefault("editTableByName", editTableByNameSQL)
        self.data.setdefault("discardTableByName", discardTableByNameSQL)

        self.data.setdefault("addColumn", addColumnSQL)
        self.data.setdefault("deleteColumn", deleteColumnSQL)
        self.data.setdefault("getColumnInfoById", getColumnInfoByIdSQL)
        self.data.setdefault("getColumnListByTableId", getColumnListByTableIdSQL)
        self.data.setdefault("getColumnListByTableName", getColumnListByTableNameSQL)
        self.data.setdefault("editColumn", editColumnSQL)
        self.data.setdefault("editColumnRemarkById", editColumnRemarkByIdSQL)
        self.data.setdefault("editColumnDiscardById", editColumnDiscardByIdSQL)

        self.data.setdefault("isInitSynchronize", isInitSynchronizeSQL)
        self.data.setdefault("getSynchronizeDatabase", getSynchronizeDatabaseSQL)
        self.data.setdefault("getSynchronizeTable", getSynchronizeTableSQL)
        self.data.setdefault("getSynchronizeColumn", getSynchronizeColumnSQL)

        self.data.setdefault("addDataRoute", addDataRouteSQL)
        self.data.setdefault("deleteDataRoute", deleteDataRouteSQL)
        self.data.setdefault("getDataRouteInfoById", getDataRouteInfoByIdSQL)
        self.data.setdefault("getDataRouteList", getDataRouteListSQL)
        self.data.setdefault("editDataRoute", editDataRouteSQL)

        self.data.setdefault("getSearchByTable", getSearchByTableSQL)
        self.data.setdefault("getSearchByTableColumn", getSearchByTableColumnSQL)
        self.data.setdefault("getSearchByColumn", getSearchByColumnSQL)




