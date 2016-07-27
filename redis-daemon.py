#!/usr/bin/env python

import redis

import sys, time
from daemon import Daemon

r = redis.StrictRedis(host='localhost', password='elenytics', port=6379, db=0)
r2 = redis.StrictRedis(host='54.149.167.108', password='elenyticsneural', port=6379, db=0)

def my_handler(message):
    with open('data.out', 'a') as file: 
        data = message['data'].split(';')
        file.write(message)
        device = message['channel']
        p2.publish(device, data)
    

p = r.pubsub(ignore_subscribe_messages=True)
p.psubscribe(**{'*': my_handler})

p2 = r2.pubsub(ignore_subscribe_messages=True)

class RedisDaemon(Daemon):
    def run(self):
        while True:
	    p.get_message()
	    time.sleep(0.005)

if __name__ == "__main__":
        daemon = RedisDaemon('/tmp/redis-daemon.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
