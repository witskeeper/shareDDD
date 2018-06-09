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
# CREATE TABLE `table_route` (
# `id` int(11) NOT NULL auto_increment,
# `route_id` int(11) default 0 NOT NULL  COMMENT '数据流Id',
# `node_id` int(11) default 0 NOT NULL  COMMENT '数据节点Id',
# `node_order` int(11) default 0 NOT NULL  COMMENT '数据节点顺序',
# `gmt_create`  timestamp default CURRENT_TIMESTAMP  COMMENT '创建时间',
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `data_node` (
# `id` int(11) NOT NULL auto_increment,
# `data_module` varchar(255)  COMMENT '节点模块',
# `data_operation` varchar(255)  COMMENT '节点操作',
# `node_built_in` TINYINT(4) default 0 NOT NULL  COMMENT '数据节点内置： 0 不内置，1 内置',
# `gmt_create`  timestamp default CURRENT_TIMESTAMP  COMMENT '创建时间',
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# INSERT INTO dba.data_node (data_module, data_operation, node_built_in, gmt_create) VALUES ('ERP', '输入流', 1, '2018-04-07 20:49:31');
# CREATE TABLE `data_route` (
# `id` int(11) NOT NULL auto_increment,
# `table_id` int(11) default 0 NOT NULL  COMMENT '数据流关联表Id',
# `gmt_create`  timestamp default CURRENT_TIMESTAMP  COMMENT '创建时间',
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
# CREATE TABLE `DBLog` (
# `id` int(11) NOT NULL auto_increment,
# `DBId` int(11) default 0 NOT NULL,
# `content` TEXT NOT NULL,
# `userId` int(11) default 0 NOT NULL,
# `gmt_create` datetime DEFAULT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
#  CREATE TABLE `column_link` (
# `id` int(11) NOT NULL auto_increment,
# `src_column_id` int(11) default 0 NOT NULL COMMENT '数据源字段Id',
# `src_table_id` int(11) default 0 NOT NULL COMMENT '数据源表Id',
# `relation_type`TINYINT(4) NOT NULL COMMENT '关系类型：0 外键关系, 1 数据关系',
# `link_column_id` int(11) default 0 NOT NULL COMMENT '关联字段Id',
# `link_table_id` int(11) default 0 NOT NULL COMMENT '关联表Id',
# `gmt_create`  timestamp default CURRENT_TIMESTAMP  COMMENT '创建时间',
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

        editTableCommentByIdSQL = """
        update dbtable set cName=%(cName)s,
        gmt_modify=now() where id=%(id)s
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
        select t.*,group_concat(concat('{"key":',t.tid,',"val":"',t.dcName,'.',t.teName,'.',t.ceName,'"}') separator '|') links from (
          select dc.*,cl.link_table_id 'tid',dm.name 'dcName',dt.eName 'teName',dc.eName 'ceName' from dbcolumn dc
          left join column_link cl on cl.src_column_id = dc.id
          left join dbcolumn dc2 on dc2.id = cl.link_column_id
          left join dbtable dt on dt.id = cl.link_table_id
          left join databasemanage dm on dm.id = dt.DBId where dc.tableId = %(tableId)s
        UNION
          select dc.*,cl.src_table_id 'tid',dm.name 'dcName',dt.eName 'teName',dc.eName 'ceName' from dbcolumn dc
          left join column_link cl on cl.link_column_id = dc.id
          left join dbcolumn dc2 on dc2.id = cl.src_column_id
          left join dbtable dt on dt.id = cl.src_table_id
          left join databasemanage dm on dm.id = dt.DBId where dc.tableId = %(tableId)s) as t
        GROUP BY t.id;
        """

        # select dc.*,group_concat(concat('{"db":',dt.DBId,',"key":',cl.link_table_id,',"val":"',dm.name,'.',dt.eName,'.',dc2.eName,'"}') separator '|') links from dbcolumn dc 
        #   left join column_link cl on cl.src_column_id = dc.id
        #   left join dbcolumn dc2 on dc2.id = cl.link_column_id
        #   left join dbtable dt on dt.id = cl.link_table_id
        #   left join databasemanage dm on dm.id = dt.DBId
        #   where dc.tableId = %(tableId)s
        #   GROUP BY dc.id


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

        editColumnTypeByIdSQL = """
        update dbcolumn set type=%(val)s, gmt_modify=now() where id=%(id)s
        """

        editColumnDiscardByIdSQL = """
        update dbcolumn set is_discarded=%(val)s, gmt_modify=now() where id=%(id)s
        """

        isInitSynchronizeSQL = """
        SELECT count(*) as tableCount from dbtable WHERE DBId = %(DBId)s
        """

        getSynchronizeDatabaseSQL = """
        SELECT TABLE_NAME,TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(schemaName)s;
        """

        getSynchronizeTableSQL = """
        SELECT COLUMN_NAME,COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schemaName)s and TABLE_NAME= %(tableName)s
        """

        getSynchronizeColumnSQL = """
        SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schemaName)s and TABLE_NAME = %(tableName)s and COLUMN_NAME = %(columnName)s
        """

        getTableCommentSQL = """
        SELECT TABLE_NAME,TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(schemaName)s
         and TABLE_NAME = %(tableName)s;
        """

        addTableRouteSQL="""
        values (%(route_id)s,%(node_id)s,%(node_order)s)
        """

        addDataNodeSQL = """
        insert into data_node (data_module,data_operation) 
        values (%(data_module)s,%(data_operation)s)
        """

        addDataRouteSQL = """
        insert into data_route (table_id) values (%(table_id)s)
        """

        getTableRouteListSQL = """
        SELECT * FROM data_route dr JOIN table_route tr on tr.route_id = dr.id
        JOIN data_node dn on dn.id = tr.node_id WHERE dr.table_id = %(table_id)s
        order by tr.route_id,tr.node_order;
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

        getSearchByColumnRemarkSQL = """
        SELECT c.id as uid, t.id,concat(t.eName,'.',c.eName,'  #',left(c.remark,15),'...') as eName from dbtable t join dbcolumn c on t.id = c.tableId 
         where DBId=%(DBId)s and c.remark like %(remark)s;
        """

        addDBLogSQL = """
        insert into dblog (DBId,content,userId,gmt_create) 
        values (%(DBId)s,%(content)s,%(userId)s,now())
        """

        getDBLogListSQL = """
        select concat(if(username is NULL,"自动",username),"在",dl.gmt_create,content) as content from dblog dl
          left join user u on u.id = dl.userId
          where DBId = %(DBId)s order by dl.gmt_create desc
        """

        addColumnLinkSQL = """
        insert into column_link (src_column_id,src_table_id,relation_type,link_column_id,link_table_id) 
        values (%(src_column_id)s,%(src_table_id)s,%(relation_type)s,%(link_column_id)s,%(link_table_id)s)
        """

        # todo 新库是子表，不要显示
        getLinkDBListSQL = """
        
        """

        getLinkTableListSQL = """
        SELECT distinct dt.id, dt.eName from column_link cl join DBTable dt on dt.id = cl.link_table_id 
        and dt.DBId = %(DBId)s;
        """

        getLinkColumnListSQL = """
        SELECT distinct dc.id, dc.eName from column_link cl join DBColumn dc on dc.id = cl.link_column_id 
        and dc.tableId = %(tableId)s;
        """

        getTableListByTableNameSQL = """
        SELECT dt.id, dt.eName from DBTable dt where
        dt.DBId = %(DBId)s and dt.eName like %(eName)s;
        """

        getColumnListByColNameSQL = """
        SELECT dc.id, dc.eName from DBColumn dc where
        dc.tableId = %(tableId)s and dc.eName like %(eName)s;
        """

        deleteColumnSQL = """
        DELETE FROM dbcolumn where tableId in (SELECT id from dbtable where DBId = %(id)s); 
        """

        deleteTableSQL = """
        DELETE FROM dbtable where DBId = %(id)s; 
        """


        #SET SQL FOR DAO
        self.data.setdefault("addTable",addTableSQL)
        self.data.setdefault("deleteTable",deleteTableSQL)
        self.data.setdefault("getTableInfoById",getTableInfoByIdSQL)
        self.data.setdefault("getTableInfoByName",getTableInfoByNameSQL)
        self.data.setdefault("getTableList", getTableListSQL)
        self.data.setdefault("editTable", editTableSQL)
        self.data.setdefault("editTableByName", editTableByNameSQL)
        self.data.setdefault("editTableCommentById", editTableCommentByIdSQL)
        self.data.setdefault("discardTableByName", discardTableByNameSQL)

        self.data.setdefault("addColumn", addColumnSQL)
        self.data.setdefault("deleteColumn", deleteColumnSQL)
        self.data.setdefault("getColumnInfoById", getColumnInfoByIdSQL)
        self.data.setdefault("getColumnListByTableId", getColumnListByTableIdSQL)
        self.data.setdefault("getColumnListByTableName", getColumnListByTableNameSQL)
        self.data.setdefault("editColumn", editColumnSQL)
        self.data.setdefault("editColumnRemarkById", editColumnRemarkByIdSQL)
        self.data.setdefault("editColumnTypeById", editColumnTypeByIdSQL)
        self.data.setdefault("editColumnDiscardById", editColumnDiscardByIdSQL)

        self.data.setdefault("isInitSynchronize", isInitSynchronizeSQL)
        self.data.setdefault("getSynchronizeDatabase", getSynchronizeDatabaseSQL)
        self.data.setdefault("getSynchronizeTable", getSynchronizeTableSQL)
        self.data.setdefault("getSynchronizeColumn", getSynchronizeColumnSQL)
        self.data.setdefault("getTableComment", getTableCommentSQL)

        self.data.setdefault("getSearchByTable", getSearchByTableSQL)
        self.data.setdefault("getSearchByTableColumn", getSearchByTableColumnSQL)
        self.data.setdefault("getSearchByColumn", getSearchByColumnSQL)
        self.data.setdefault("getSearchByColumnRemark", getSearchByColumnRemarkSQL)

        self.data.setdefault("addDBLog", addDBLogSQL)
        self.data.setdefault("getDBLogList", getDBLogListSQL)

        self.data.setdefault("addColumnLink", addColumnLinkSQL)
        self.data.setdefault("getLinkTableList", getLinkTableListSQL)
        self.data.setdefault("getLinkColumnList", getLinkColumnListSQL)
        self.data.setdefault("getTableListByTableName", getTableListByTableNameSQL)
        self.data.setdefault("getColumnListByColName", getColumnListByColNameSQL)

        self.data.setdefault("addTableRoute", addTableRouteSQL)
        self.data.setdefault("addDataNode", addDataNodeSQL)
        self.data.setdefault("addDataRoute", addDataRouteSQL)
        self.data.setdefault("getTableRouteList", getTableRouteListSQL)

        self.data.setdefault("deleteColumn", deleteColumnSQL)
        self.data.setdefault("deleteTable", deleteTableSQL)




