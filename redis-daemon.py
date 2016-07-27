#!/usr/bin/env python

import redis

import sys, time
from daemon import Daemon

r = redis.StrictRedis(host='localhost', password='elenytics', port=6379, db=0)
r2 = redis.StrictRedis(host='54.149.167.108', password='elenyticsneural', port=6379, db=0)

def my_handler(message):
    with open('data.out', 'a') as file: 
        data = message['data'].split(';')
        file.write('%s' % ' '.join(map(str, data)))
        file.write('\n')
        device = message['channel']
        r2.publish(device, ' '.join(map(str, data)))
    return True
    

p = r.pubsub(ignore_subscribe_messages=True)
p.psubscribe(**{'*': my_handler})

p2 = r2.pubsub(ignore_subscribe_messages=True)
p2.psubscribe(**{'*': my_handler})

class RedisDaemon(Daemon):
    def run(self):
        while True:
	    p.get_message()

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
