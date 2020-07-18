import redis
import threading
import requests

endpoint = "http://127.0.0.1:8000"

#result = requests.get(endpoint)
#print(result)

redis = redis.Redis(host="localhost", port = 6379)

def msg_server(server, data):
    resp = requests.get(server, data)
    print(f'{resp} is the server response for {data} being pushed')

while True:
    try:
        data = redis.zrange('queue',-1,-1)
        if len(data):
            #print(data[0])
            redis.zrem('queue',data[0])
            t = threading.Thread(target = msg_server, args = [endpoint, data[0]])
            t.start()
    except:
        print('ERROR!')
        pass
