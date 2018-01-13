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

def start_server():
    
    app = tornado.web.Application(handlers=[
              #route
              (r"/v1/user/(.*)",UserHandler),
              (r"/v1/project/(.*)",ProjectHandler),
              (r"/v1/env/(.*)",EnvironmentHandler),
              (r"/v1/group/(.*)",GroupHandler)
              ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(SystemConfig.httpPost)

    tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
    start_server()
