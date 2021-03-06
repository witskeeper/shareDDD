CREATE TABLE `user` (
`id` int(11) NOT NULL auto_increment,
`username` varchar(255) NOT NULL unique,
`passwd` varchar(255) NOT NULL,
`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
`remarks` varchar(255) default NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

ALTER TABLE `user` ADD unique(`username`);

CREATE TABLE `environment` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL unique,
`url` varchar(255) default NULL,
`create_userid` int(11) default NULL,
`create_username` varchar(255) default NULL,
`datatemplate` longtext default NULL,
`dbname` varchar(255) DEFAULT NULL,
`dbhostname` varchar(255) DEFAULT NULL,
`dbport` varchar(255) DEFAULT NULL,
`dbusername` varchar(255) DEFAULT NULL,
`dbpasswd` varchar(255) DEFAULT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

ALTER TABLE `environment` ADD unique(`name`);

CREATE TABLE `project` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL unique,
`create_userid` int(11) NOT NULL,
`create_username` varchar(255) NOT NULL,
`version` varchar(255) DEFAULT NULL,
`remarks` varchar(255) DEFAULT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

ALTER TABLE `project` ADD unique(`name`);

CREATE TABLE `group_info` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL,
`create_userid` int(11) NOT NULL,
`type` tinyint(4) DEFAULT 0 COMMENT '0: api 1: case',
`projectid` int(11) NOT NULL,
`parent_groupid` int(11) DEFAULT 0,
`ischild` tinyint(4) DEFAULT 0 COMMENT '0:not child 1:is child',
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `interface` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL,
`url` varchar(255) NOT NULL,
`create_userid` int(11) NOT NULL,
`create_username` varchar(255) NOT NULL,
`update_userid` int(11) DEFAULT NULL,
`update_username` varchar(255) DEFAULT NULL,
`interface_describe` varchar(255) DEFAULT NULL,
`params` text DEFAULT NULL,
`success_response` text DEFAULT NULL,
`failure_response` text DEFAULT NULL,
`method` tinyint(4) NOT NULL COMMENT '0: GET 1: POST 2.PUT 3. DELETE',
`format` tinyint(4) NOT NULL COMMENT '0: form-data 1: json',
`response_type` tinyint(4) default 0 COMMENT '0: json 1: view',
`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
`remarks` varchar(255) DEFAULT NULL,
`projectid` int(11) NOT NULL,
`groupid` int(11) NOT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `testcase` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL,
`create_userid` int(11) NOT NULL,
`create_username` varchar(255) NOT NULL,
`update_userid` int(11) NOT NULL,
`update_username` varchar(255) NOT NULL,
`case_describe` varchar(255) NOT NULL,
`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
`remarks` varchar(255) DEFAULT NULL,
`projectid` int(11) NOT NULL,
`groupid` int(11) NOT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `casecontent` (
`id` int(11) NOT NULL auto_increment,
`step_name` varchar(255) NOT NULL,
`caseid` int(11) NOT NULL,
`step` int(11) NOT NULL,
`interfaceid` int(11) DEFAULT NULL,
`url` varchar(255) DEFAULT NULL,
`method` tinyint(4) DEFAULT NULL COMMENT '0: GET 1: POST 2.PUT 3. DELETE',
`format` tinyint(4) DEFAULT NULL COMMENT '0: form-data 1: json',
`request_params` varchar(255) DEFAULT NULL,
`timeout` int(11) DEFAULT NULL,
`type` tinyint(4) default 0 COMMENT '0: api 1: sql',
`sqlcontent` varchar(255) DEFAULT NULL,
`response_type` tinyint(4) DEFAULT '0' COMMENT '0: json 1: view',
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `assert` (
`id` int(11) NOT NULL auto_increment,
`casecontentid` int(11) NOT NULL,
`actual` varchar(255) NOT NULL,
`expect` varchar(255) DEFAULT NULL,
`assert_type` varchar(255) NOT NULL COMMENT '0: equal 1: not equal 2: contain 3:not contain ',
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `testsuite` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL unique,
`testcaseids` text DEFAULT NULL,
`create_userid` int(11) NOT NULL,
`create_username` varchar(255) NOT NULL,
`update_userid` int(11) NOT NULL,
`update_username` varchar(255) NOT NULL,
`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
`remarks` varchar(255) DEFAULT NULL,
`envid` int(11) DEFAULT NULL,
`projectid` int(11) DEFAULT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

ALTER TABLE `testsuite` ADD unique(`name`);

CREATE TABLE `testcaseinstance` (
`id` int(11) NOT NULL auto_increment,
`create_userid` int(11) NOT NULL,
`create_username` varchar(255) NOT NULL,
`suite_name` varchar(255) NOT NULL,
`suite_id` int(11) NOT NULL,
`status` varchar(255) NOT NULL COMMENT 'wait,run,stop,fail,success,timeout,error',
`build_start` datetime DEFAULT NULL,
`build_end` datetime DEFAULT NULL,
`trigger_type` tinyint(4) default 0 COMMENT '0: manual 1: ci 2:crontab',
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `caseresult` (
`id` int(11) NOT NULL auto_increment,
`instanceid` int(11) NOT NULL,
`caseid` int(11) NOT NULL,
`casename` varchar(255) NOT NULL,
`runtime` int(11) DEFAULT NULL,
`status` varchar(255) NOT NULL COMMENT 'wait,run,stop,fail,success,timeout,error',
`exec_start` datetime DEFAULT NULL,
`exec_end` datetime DEFAULT NULL,
`message` text DEFAULT NULL,
`remarks` varchar(255) DEFAULT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `taskmetaqinfo` (
`id` int(11) NOT NULL auto_increment,
`instanceid` int(11) NOT NULL,
`status` varchar(255) NOT NULL COMMENT '0 wait 1 send 2 receive',
`running_consumer` varchar(255) DEFAULT NULL,
`msg_id` varchar(255) DEFAULT NULL COMMENT 'process id',
`message` text DEFAULT NULL,
`is_deleted` tinyint(4) DEFAULT 0,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `session_manage` (
`id` int(11) NOT NULL auto_increment,
`user_id` int(11) NOT NULL,
`session` varchar(255) NOT NULL,
`domain` varchar(255) DEFAULT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# add
CREATE TABLE `databaseManage` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL,
`host` varchar(255) NOT NULL,
`port` int(4) default 0 NOT NULL,
`username` varchar(32) NOT NULL,
`password` varchar(128) NOT NULL,
`schemaName` varchar(32) NOT NULL,
`businessUnit` TINYINT(4) default 0 NOT NULL,
`productUnit` TINYINT(4) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tableGroup` (
`id` int(11) NOT NULL auto_increment,
`DBId` int(11) default 0 NOT NULL,
`name` varchar(64) NOT NULL,
`isDefault` TINYINT(4) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tableGroupRelation` (
`id` int(11) NOT NULL auto_increment,
`tableId` int(11) default 0 NOT NULL,
`groupId` int(11) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `databaseManage` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) NOT NULL,
`host` varchar(255) NOT NULL,
`port` int(4) default 0 NOT NULL,
`username` varchar(32) NOT NULL,
`password` varchar(128) NOT NULL,
`schemaName` varchar(32) NOT NULL,
`businessUnit` TINYINT(4) default 0 NOT NULL,
`productUnit` TINYINT(4) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tableGroup` (
`id` int(11) NOT NULL auto_increment,
`DBId` int(11) default 0 NOT NULL,
`name` varchar(64) NOT NULL,
`isDefault` TINYINT(4) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tableGroupRelation` (
`id` int(11) NOT NULL auto_increment,
`tableId` int(11) default 0 NOT NULL,
`groupId` int(11) default 0 NOT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `DBTable` (
`id` int(11) NOT NULL auto_increment,
`DBId` int(11) default 0 NOT NULL,
`cName` varchar(255) NOT NULL,
`eName` varchar(255) NOT NULL,
`remark` varchar(1024) NOT NULL,
`is_discarded` TINYINT(4)  NOT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `DBColumn` (
`id` int(11) NOT NULL auto_increment,
`tableId` int(11) default 0 NOT NULL,
`cName` varchar(255) NOT NULL,
`eName` varchar(255) NOT NULL,
`type` varchar(32) NOT NULL,
`remark` varchar(1024)  NOT NULL,
`is_discarded` TINYINT(4)  NOT NULL,
`gmt_create` datetime DEFAULT NULL,
`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `dataRoute` (
`id` int(11) NOT NULL auto_increment,
`tableId` int(11) default 0 NOT NULL,
`route` varchar(512) NOT NULL,
`type` TINYINT(4) NOT NULL COMMENT '0 input, 1 output',
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `DBLog` (
`id` int(11) NOT NULL auto_increment,
`DBId` int(11) default 0 NOT NULL,
`content` TEXT NOT NULL,
`userId` int(11) default 0 NOT NULL,
`gmt_create` datetime DEFAULT NULL,
PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

