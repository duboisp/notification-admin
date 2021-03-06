import os
import sys
import traceback

workers = 5
worker_class = "eventlet"
bind = "0.0.0.0:{}".format(os.getenv("PORT"))
accesslog = '-'


def on_starting(server):
    server.log.info("Starting Notifications Admin")


def worker_abort(worker):
    worker.log.info("worker received ABORT {}".format(worker.pid))
    for threadId, stack in sys._current_frames().items():
        worker.log.error(''.join(traceback.format_stack(stack)))


def on_exit(server):
    server.log.info("Stopping Notifications Admin")


def worker_int(worker):
    worker.log.info("worker: received SIGINT {}".format(worker.pid))
