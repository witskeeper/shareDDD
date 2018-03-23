# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from src.main.master.common.constants import SystemConfig
from src.main.master.controller.UserController import UserHandler
from src.main.master.controller.ProjectController import ProjectHandler
from src.main.master.controller.EnvironmentController import EnvironmentHandler
from src.main.master.controller.GroupController import GroupHandler
from src.main.master.controller.InterfaceController import InterfaceHandler
from src.main.master.controller.CaseContentController import CaseContentHandler
from src.main.master.controller.TestCaseController import TestCaseHandler
from src.main.master.controller.AssertController import AssertHandler
from src.main.master.controller.TestSuiteController import TestSuiteHandler
from src.main.master.controller.TestCaseInstanceController import TestCaseInstanceHandler
from src.main.master.controller.DatabaseController import DatabaseHandler
from src.main.master.controller.ProductController import ProductHandler
from src.main.master.controller.TableController import TableHandler

def start_server():
    
    app = tornado.web.Application(handlers=[
              #route
              (r"/v1/user/(.*)",UserHandler),
              (r"/v1/project/(.*)",ProjectHandler),
              (r"/v1/env/(.*)",EnvironmentHandler),
              (r"/v1/group/(.*)",GroupHandler),
              (r"/v1/interface/(.*)",InterfaceHandler),
              (r"/v1/case/(.*)", TestCaseHandler),
              (r"/v1/content/(.*)", CaseContentHandler),
              (r"/v1/assert/(.*)", AssertHandler),
              (r"/v1/suite/(.*)", TestSuiteHandler),
              (r"/v1/instance/(.*)", TestCaseInstanceHandler),
              (r"/v1/database/(.*)", DatabaseHandler),
              (r"/v1/product/(.*)", ProductHandler),
              (r"/v1/table/(.*)", TableHandler),
              ])

    http_server = tornado.httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(SystemConfig.httpPost)

    tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
    start_server()
