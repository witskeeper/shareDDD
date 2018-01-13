# -*- coding: utf-8 -*-

#CREATE TABLE `testcase` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`update_userid` int(11) NOT NULL,
#`update_username` varchar(255) NOT NULL,
#`describe` varchar(255) NOT NULL,
#`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
#`remarks` varchar(255) DEFAULT NULL,
#`projectid` int(11) NOT NULL,
#`groupid` int(11) NOT NULL,
#`envid` int(11) NOT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class TestCaseSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTestCaseSQL="""
        insert into testcase (name,create_userid,create_username,update_userid,update_username,
        describe,status,remarks,projectid,groupid,envid,gmt_create) values (%(name)s,%(userId)s,%(userName)s,
        %(userId)s,%(userName)s,describe,status,remarks,projectid,groupid,envid,now())
        """
        deleteTestCaseSQL="""
        delete from testcase where id = %(groupId)s
        """
        updateTestCaseSQL="""
        update testcase (name,create_userid,create_username,update_userid,update_username,
        describe,status,remarks,projectid,groupid,envid,gmt_create) values (%(name)s,%(userId)s,%(userName)s,
        %(userId)s,%(userName)s,describe,status,remarks,projectid,groupid,envid,now())
        """
        getGroupInfoByProjectIdSQL="""
        select * from testcase where projectid = %(projectId)s and type = %(type)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addGroup",addGroupSQL)
        self.data.setdefault("deleteGroup",deleteGroupSQL)
        self.data.setdefault("getGroupInfoByProjectId",getGroupInfoByProjectIdSQL)

