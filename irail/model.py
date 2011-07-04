# -*- coding: utf-8 -*-

# Copyright (c) 2011, Wouter Horré
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

class Test(object):
  def repr__(self):
    return '<%s>' % str('\n '.join('%s : %s' %
      (k, repr(v)) for (k, v) in self.__dict.iteritems()))

# I wrote object_factory so I don't have to define a seperate class
# for every return type of a api method.
# TODO put in class with prity __repr__ and __str__
def object_factory(d):
  """object_factory will create an object from a dict or a seq"""
  new = type('obj', (object,), d)
  seqs = tuple, list, set, frozenset # all the sequence types
  for k, v in d.iteritems():
    if isinstance(v, dict):
      setattr(new, k, object_factory(v))
    elif isinstance(v, seqs):
      setattr(new, k, type(v)(object_factory(i) if isinstance(i, dict) else i for i in v))
    else:
      setattr(new, k, v)
  return new
  
class ResultList:
  def __init__(self, timestamp, version):
    self.__timestamp = timestamp
    self.__version = version

  def timestamp(self):
    return self.__timestamp

  def version(self):
    return self.__version

class StationList(ResultList):

  def __init__(self, timestamp, version, stations):
    self.__stations = stations
    ResultList.__init__(self, timestamp, version)

  def stations(self):
    return self.__stations

class Station:

  def __init__(self, name, standardname, id, locationX, locationY):
    self.__name = name
    self.__standardname = standardname
    self.__id = id
    self.__locationX = locationX
    self.__locationY = locationY

  def name(self):
    return self.__name

  def standardname(self):
    return self.__standardname

  def id(self):
    return self.__id

  def locationX(self):
    return self.__locationX

  def locationY(self):
    return self.__locationY

  def __str__(self):
    return "Station " + self.id() + " | " + self.name() + " @ (" + self.locationY() + "," + self.locationX() + ")"

class ConnectionList(ResultList):

  def __init__(self, timestamp, version, connections):
    self.__connections = connections
    ResultList.__init__(self, timestamp, version)

  def connections(self):
    return self.__connections

class Connection:

    def __init__(self, id, departure, vias, arrival, duration):
      self.__id = id
      self.__departure = departure
      self.__vias = vias
      self.__arrival = arrival
      self.__duration = duration

    def id(self):
      return self.__id

    def departure(self):
      return self.__departure

    def vias(self):
      return self.__vias

    def arrival(self):
      return self.__arrival

    def duration(self):
      return self.__duration

    def __str__(self):
      s = """Connection ({0}):
  departure: {1}
  arrival: {2}
  vias: {3}
  duration: {4}"""
      return s.format(self.id(), self.departure(), self.arrival(), self.vias(), self.duration())

class ConnectionEvent:

  def __init__(self, station, platform, time, delay, vehicle, direction):
    self.__station = station
    self.__platform = platform
    self.__time = time
    self.__delay = delay
    self.__vehicle = vehicle
    self.__direction = direction

  def station(self):
    return self.__station

  def platform(self):
    return self.__platform

  def time(self):
    return self.__time

  def delay(self):
    return self.__delay

  def vehicle(self):
    return self.__vehicle

  def direction(self):
    return self.__direction

  def __str__(self):
    s = """@{0} (+{1}) -> {2}"""
    return s.format(self.time(), self.delay(), self.station()) 

class Arrival(ConnectionEvent):
  
  def __init__(self, station, platform, time, delay, vehicle, direction):
    ConnectionEvent.__init__(self, station, platform, time, delay, vehicle, direction)

 
class Departure(ConnectionEvent):

  def __init__(self, station, platform, time, delay, vehicle, direction):
    ConnectionEvent.__init__(self, station, platform, time, delay, vehicle, direction)

