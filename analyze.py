import sys, time
import numpy

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

for ap in aps:
    print ap
    print ', '.join(map(str, aps[ap]))

for rssi in aps.itervalues():
    arr = numpy.array(rssi).astype(numpy.float)
    print numpy.std(arr)
