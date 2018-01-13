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
        describe,status,remarks,projectid,groupid,envid,gmt_create) 
        values 
        (%(name)s,%(userId)s,%(userName)s,%(userId)s,%(userName)s,%(describe)s,
        %(status)s,%(remarks)s,%(projectId)%,%(groupId)s,%(envId)s,now())
        """
        deleteTestCaseSQL="""
        delete from testcase where id = %(caseId)s
        """
        updateTestCaseSQL="""
        update testcase set name=%(name)s,update_userid=%(userId)s,update_username=%(userName)s,
        describe=%(describe)s,status=%(status)s,remarks=%(remarks)s,envid=%(envid)s where id=%(caseId)s
        """
        getCaseInfosByConditionSQL="""
        select * from testcase where projectid = %(projectId)s and groupid= %(groupId)s 
        order by id desc limit %(offset)s,%(limit)s 
        """
        getCaseInfosByIdSQL="""
        select * from testcase where id=%(caseId)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addTestCase",addTestCaseSQL)
        self.data.setdefault("deleteTestCase",deleteTestCaseSQL)
        self.data.setdefault("updateTestCase",updateTestCaseSQL)
        self.data.setdefault("getCaseInfosByCondition", getCaseInfosByConditionSQL)
        self.data.setdefault("getCaseInfosById", getCaseInfosByIdSQL)

