#!/usr/bin/env python

# coding: utf-8
# Copyright 2022 Johnson Zhao
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#

# remember to:
#     pip install flask

import flask
from flask import Flask, request, render_template, redirect
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }
#
# entity is player? e.g. 'a' 
# value of play key is dict of coords e.g. {'x':1, 'y':2}
class World:
    def __init__(self):
        self.clear()
        
    # {
    #    'a':{'x':1, 'y':2},
    #    'b':{'x':2, 'y':3}
    # }
    #
    # 'a'               = entity
    # {'x':2, 'y':3}    = entry
    # 'x' and 'y'       = key
    # 2 and 3           = value
    def update(self, entity, key, value):
        entry = self.space.get(entity, dict())
        entry[key] = value
        self.space[entity] = entry

    # data would be dict/json
    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity, dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])


def json_wrap(data):
    wrapped_data = json.dumps(data)
    #wrapped_data = json.loads(wrapped_data)
    return wrapped_data


@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    # https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    return redirect('static/index.html', code=301)


@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    # should return json data for a single entitiy?
    req_json = flask_post_json()
    print('update request json:\n' + str(req_json))
    myWorld.set(entity=entity, data=req_json)
    payload = myWorld.get(entity=entity)
    payload = json_wrap(payload)
    return payload


@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    # Returns json representing whole world
    world_dict = myWorld.world()
    payload = json_wrap(world_dict)
    return payload


@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    # Return json of single entity
    entity_dict = myWorld.get(entity=entity)
    payload = json_wrap(entity_dict)   
    return payload


@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    # Clears the browser window
    myWorld.clear()
    payload = json_wrap(myWorld.world()) 
    return payload


if __name__ == "__main__":
    app.run()
