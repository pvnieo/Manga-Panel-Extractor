import os

from dotenv import load_dotenv
from redis import Redis
from rq import Connection, Queue, Worker

load_dotenv()

listen = [os.environ.get('QUEUE_NAME')]

redis_conn = Redis(
  host= os.environ.get('REDIS_HOST'),
  port= '31538',
  password= os.environ.get('REDIS_PASS'),
)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()