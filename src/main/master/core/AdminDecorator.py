# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult

#set log
logger = Log('AdminDecorator')
logger.write_to_file(SystemConfig.logPathPrefix+"AdminDecorator.log")

class AdminDecoratorServer(object):

    def __init__(self):
        pass

    @staticmethod
    def execImplDecorator():
        def _deco(func):
            def __deco(*args,**kwargs):
                try:
                    return func(*args,**kwargs)
                except Exception,err:
                    dataResult = DataResult()
                    logger.error(traceback.format_exc())
                    dataResult.setMessage(traceback.format_exc())
                    dataResult.setSuccess(False)
                    dataResult.setStatusCode(500)
                    return dataResult
            return __deco
        return _deco

