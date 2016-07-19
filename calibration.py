import redis

import sys, time

import json

import datetime

r = redis.StrictRedis(host='localhost', password="elenytics", port=6379, db=0)

def my_handler(message):
	with open('inputs.out', 'a') as file:
                print message
                print datetime.datetime.time(datetime.datetime.now())
		#json.dump(message['data'], file, indent=2)
		data = message['data'].split(';')
                battery_level = data[-1]
                del data[-1]
		file.write('%s' % ','.join(map(str, data)))
		file.write('\n')


p = r.pubsub(ignore_subscribe_messages=True)
p.psubscribe(**{'*': my_handler})

def get_messages(x, y, floor):
    outputs = open('outputs.out', 'a')
    outputs.write("{}, {}, {}".format(x,y,floor))
    outputs.write('\n')
    outputs.close()

    inputs = open('inputs.out', 'a')
    inputs.write('\n')
    inputs.close()

    try:
        while True:
            p.get_message()
            time.sleep(0.005)
    except KeyboardInterrupt:
       return True 

while True:
    x = input("Enter x: ")
    y = input("Enter y: ")
    floor = input("Enter floor: ")
    get_messages(x, y, floor)

