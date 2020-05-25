import os
import redis
from rq import Worker, Queue, Connection

listen = ['yeetcode-judge']

conn = redis.from_url('redis://')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work(logging_level='WARN')



