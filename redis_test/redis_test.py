# 使用方式1(依赖django
from django_redis import get_redis_connection

cache = get_redis_connection()

cache.set('name', 'sewell')

cache.get('name')

# 使用方式2
import redis
cache = redis.Redis(host='localhost', port=6379, password='root')
cache.get('name')

import json
data = json.dumps({'age': 18})
cache.set('data', data)

