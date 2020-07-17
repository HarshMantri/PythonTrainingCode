import redis
import random
import uuid

def main():
    r = redis.Redis(host='localhost', port=6379)
    while True:
        r.zincrby('queue', 1, str(uuid.uuid1()))

if __name__ == "__main__":
    main()

