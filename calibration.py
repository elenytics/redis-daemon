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

try: 
    while True:
        x = input("Enter x: ")
        y = input("Enter y: ")
        floor = input("Enter floor: ")
        get_messages(x, y, floor)
except KeyboardInterrupt:
    with open('inputs.out', 'r') as inputs:
        lines = [line.rstrip('\n') for line in open('inputs.out')]

    data = []
    for line in lines:
        data.append(line.split('  '))

    pairs = []
    for line in data:
        for pair in line:
            pairs.append(pair.split(','))

    for pair in pairs:
        if len(pair) > 2:
            del pair[-1]

    pairs = [pair for pair in pairs if pair != ['']]

    aps = {}

    for pair in pairs:
        if pair[0] not in aps:
            aps[pair[0]] = [pair[1]]
        else:
            aps[pair[0]].append(pair[1])

    data = open('data.out', 'a')
    for ap in aps:
        open.write(ap)
        open.write(', '.join(map(str, aps[ap]))