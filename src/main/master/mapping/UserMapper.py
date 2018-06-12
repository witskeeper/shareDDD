# -*- coding: utf-8 -*-
#CREATE TABLE `user` (
#`id` int(11) NOT NULL auto_increment,
#`username` varchar(255) NOT NULL unique,
#`passwd` varchar(255) NOT NULL,
#`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
#`remarks` varchar(255) default NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

#ALTER TABLE `user` ADD unique(`username`);

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
        insert into user (username,passwd,remarks,gmt_create) values (%(userName)s,%(userPasswd)s,%(remarks)s,now())
        """
        getUserInfoSQL="""
        select id,username,passwd,remarks from user where username= %(userName)s and status = 0
        """
        deleteUserInfoSQL="""
        delete from user where id = %(userId)s
        """
        getUserInfoByIdSQL="""
        select username,passwd,remarks,status from user where id = %(userId)s
        """
        deleteUserInfoByNameSQL="""
        delete from user where username = %(userName)s
        """
        addSysUserSQL = """
                insert into user_sys (username,mobile,userid,unionid,openid,department_id,roles,gmt_create) values (%(userName)s,%(mobile)s,%(userid)s,(unionid)s,%(openid)s,%(department_id)s,%(roles)s,now())
                """
        getSysUserListSQL = """
                select id,username,department_id,roles from user_sys where status = 0
                """
        deleteSysUserInfoSQL = """
                delete from user_sys where id = %(Id)s
                """
        getSysUserInfoByNameSQL = """
                select username,mobile,userid,department_id,roles,status from user_sys where username = %(userName)s
                """
        deleteSysUserInfoByNameSQL = """
                delete from user_sys where username = %(userName)s
                """

        #SET SQL FOR DAO
        self.data.setdefault("addUser",addUserSQL)
        self.data.setdefault("getUserInfo", getUserInfoSQL)
        self.data.setdefault("deleteUser", deleteUserInfoSQL)
        self.data.setdefault("getUserInfoById", getUserInfoByIdSQL)
        self.data.setdefault("deleteUserInfoByName",deleteUserInfoByNameSQL)
        self.data.setdefault("addSysUser", addSysUserSQL)
        self.data.setdefault("getSysUserList", getSysUserListSQL)
        self.data.setdefault("deleteSysUser", deleteSysUserInfoSQL)
        self.data.setdefault("getSysUserInfoByName", getSysUserInfoByNameSQL)
        self.data.setdefault("deleteSysUserInfoByName", deleteSysUserInfoByNameSQL)