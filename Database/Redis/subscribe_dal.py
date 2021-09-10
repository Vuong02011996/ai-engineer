import redis
import datetime

REDIS_HOST = "14.224.128.168"
REDIS_PORT = 63799
REDIS_PASSWORD = "Q2xvdmVyQDEyMw=="
REDIS_DB = 0

client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
pubsub = client.pubsub()

# pubsub.subscribe('image_grouping_test')
pubsub.subscribe('register_channel_test')

while True:
    for message in pubsub.listen():
        print(datetime.datetime.now())
        print(message["data"])