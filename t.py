from rq import Queue
from redis import Redis
import requests
from test import count_words_at_url
import time

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
job = q.enqueue(count_words_at_url, 'http://nvie.com')

while job.result == None:
    print(job.result)   # => None
print(job.result)

