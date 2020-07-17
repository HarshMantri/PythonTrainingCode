import redis
import threading
import requests

endpoint = "http://127.0.0.1:8000"

result = requests.get(endpoint)
print(result)


redis = redis.Redis(host="localhost", port = 6379)

while True:
    try:
        data = redis.zrange('queue',-1,-1)
        if len(data):
            print(data[0])
            redis.zrem('queue',data[0])
            resp = requests.get(endpoint, data[0])
            print(resp)
    except:
        print('ERROR!')
        pass
