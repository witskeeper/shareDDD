# -*- coding: utf-8 -*-

#CREATE TABLE `group_info` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL,
#`create_userid` int(11) NOT NULL,
#`type` tinyint(4) default 0 COMMENT '0: api 1: case',
#`projectid` int(11) NOT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class GroupSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addGroupSQL="""
        insert into group_info (name,create_userid,type,projectid,gmt_create) values (%(name)s,%(userId)s,%(type)s,%(projectId)s,now())
        """
        deleteGroupSQL="""
        delete from group_info where id = %(groupId)s
        """
        getGroupInfoByProjectIdSQL="""
        select * from group_info where projectid = %(projectId)s and type = %(type)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addGroup",addGroupSQL)
        self.data.setdefault("deleteGroup",deleteGroupSQL)
        self.data.setdefault("getGroupInfoByProjectId",getGroupInfoByProjectIdSQL)

