# -*- coding: utf-8 -*-

class UserSQLMapper:

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
        insert into user (userName,phone,sex,Gmt) values (%(user_name)s,%(user_phone)s,%(user_sex)s,now())
        """
        getUserInfoSQL="""
        select * from user where userName= %(user_name)s
        """
        deleteUserInfoSQL="""
        delete from user where userName= %(user_name)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addUser",addUserSQL)
        self.data.setdefault("getUserInfo", getUserInfoSQL)
        self.data.setdefault("deleteUser", deleteUserInfoSQL)
