# -*- coding: utf-8 -*-

class LoginSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addUserSQL="""
        insert into user (username,passwd,remarks,gmt_create) values (%(userName)s,%(userPasswd)s,%(remarks)s,now())
        """

        #SET SQL FOR DAO
        self.data.setdefault("addUser",addUserSQL)

