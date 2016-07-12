import redis

import sys, time

import json

r = redis.StrictRedis(host='localhost', password="elenytics", port=6379, db=0)

def my_handler(message):
	with open('calibration.out', 'a') as file:
		#json.dump(message['data'], file, indent=2)
		data = message['data'].split(';')
		file.write('%s' % ', '.join(map(str, data)))
		file.write('\n')


p = r.pubsub(ignore_subscribe_messages=True)
p.psubscribe(**{'*': my_handler})

while True:
	p.get_message()
	time.sleep(0.005)
