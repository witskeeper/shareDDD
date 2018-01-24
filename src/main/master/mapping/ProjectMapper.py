# -*- coding: utf-8 -*-

#CREATE TABLE `project` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL unique,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`version` varchar(255) DEFAULT NULL,
#`remarks` varchar(255) DEFAULT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

#ALTER TABLE `project` ADD unique(`name`);

class ProjectSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addProjectSQL="""
        insert into project (name,create_username,create_userid,version,remarks,gmt_create) values (%(name)s,%(userName)s,%(userId)s,%(version)s,%(remarks)s,now())
        """
        getProjectInfoByNameSQL="""
        select * from project where name = %(name)s
        """
        deleteProjectSQL="""
        delete from project where id = %(projectId)s
        """
        getProjectInfoByIdSQL="""
        select * from project where id = %(projectId)s
        """
        getProjectListSQL="""
        select * from project
        """

        #SET SQL FOR DAO
        self.data.setdefault("addProject",addProjectSQL)
        self.data.setdefault("getProjectInfoByName",getProjectInfoByNameSQL)
        self.data.setdefault("deleteProject",deleteProjectSQL)
        self.data.setdefault("getProjectInfoById",getProjectInfoByIdSQL)
        self.data.setdefault("getProjectList", getProjectListSQL)

