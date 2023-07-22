import os

import redis

redis_host = os.environ.get('REDIS_HOST')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
