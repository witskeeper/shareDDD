# -*- coding: utf-8 -*-

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
        insert into project (name,createuserid,createtime,version) values (%(name)s,%(createuserid)s,now(),%(version)s)
        """
        editProjectSQL="""
        update 
        """

        getProjectInfoByNameSQL="""
        select * from project where name = %(name)s
        """
        deleteProjectSQL="""
        delete from project where id = %(projectid)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addProject",addProjectSQL)
        self.data.setdefault("getProjectInfoByName",getProjectInfoByNameSQL)
        self.data.setdefault("deleteProject",deleteProjectSQL)
        self.data.setdefault("editProject",editProjectSQL)

