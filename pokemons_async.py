#!/usr/bin/env python
import requests
from collections import defaultdict
import gevent
from gevent.queue import Queue
from gevent.pool import Pool
import gevent.monkey; gevent.monkey.patch_socket()

# http://pokeapi.co/

#optimise mapreduce

BASE_URL = 'http://pokeapi.co/'

pool = gevent.pool.Pool(50)

responses = []
completed = 0

pokedex_response = requests.get(BASE_URL + 'api/v1/pokedex/1/')
objects = pokedex_response.json()
moves_count = defaultdict(int)

def async_request(r):
    resp = requests.get(r)
    responses.append(resp)
    gevent.sleep(0)

def move_counter(resp):
    p_object = resp.json()
    moves = p_object['moves']
    for m in moves:
        moves_count[m['name']] += 1
    completed =+ 1

i = 0
for i, o in enumerate(objects['pokemon']):
   r = BASE_URL + o['resource_uri']
   print 'requesting {0}\r'.format(r)
   pool.spawn(async_request, r)
pool.join()

for r in responses:
    move_counter(r)

# converts moves dict into a list of tuples and sorts by tuples second value
#sorted_moves = sorted(moves_count.items(), key=operator.itemgetter(1))
# not as efficient?
sorted_moves = sorted(moves_count, key=moves_count.get)

# just getting the move off the top of the list
most_popular_move = sorted_moves[len(sorted_moves) - 1]

print 'total pokemons counted: {0}'.format(len(responses))
print 'total moves counted: {0}'.format(len(sorted_moves))
print most_popular_move, moves_count[most_popular_move]
