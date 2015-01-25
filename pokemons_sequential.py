#!/usr/bin/env python
import requests
from collections import defaultdict

# http://pokeapi.co/

# incorporate gevent

#optimise mapreduce

BASE_URL = 'http://pokeapi.co/'
LIMIT = 50

pokedex_response = requests.get(BASE_URL + 'api/v1/pokedex/1/')
objects = pokedex_response.json()
moves_count = defaultdict(int)

i = 0
while i < LIMIT:
    for o in objects['pokemon']:

        if i >= LIMIT:
            break

        # this response goes into a gevent.request
        pokemon_response = requests.get(BASE_URL + o['resource_uri'])

        # this is the handler
        pokemon_object = pokemon_response.json()

        print "counting: " + pokemon_object['name']
        moves = pokemon_object['moves']

        for m in moves:
            moves_count[m['name']] += 1
        i += 1
        #end of handler

# converts moves dict into a list of tuples and sorts by tuples second value
#sorted_moves = sorted(moves_count.items(), key=operator.itemgetter(1))
# not as efficient?
sorted_moves = sorted(moves_count, key=moves_count.get)
# just getting the move off the top of the list
most_popular_move = sorted_moves[len(sorted_moves) - 1]

print most_popular_move
