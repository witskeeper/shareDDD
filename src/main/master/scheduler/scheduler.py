# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler

#test
#TODO
def my_job():
    print "hello test"

sched = BlockingScheduler()
sched.add_job(my_job,'interval',seconds=200)
sched.start()